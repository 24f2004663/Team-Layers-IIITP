from app.main import app
from app.api.deps import get_db
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.infrastructure.database.base import Base
import asyncio

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

async def init_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_test_db())

test_session_local = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def override_get_db():
    async with test_session_local() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_check_endpoint():
    """Verify health check endpoint returns 200 and valid JSON data."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"
    assert "components" in json_data

def test_auth_and_user_flow():
    """Verify registration, login, and profile fetching sequence."""
    import uuid
    user_email = f"test_api_user_flow_{uuid.uuid4()}@lifegps.com"
    
    # 1. Register User
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": user_email,
            "password": "strongpassword123",
            "full_name": "API Flow Tester",
            "archetype": "Architect",
            "core_values": ["growth"],
            "strengths": ["logic"],
            "weaknesses": ["experience"]
        }
    )
    assert register_response.status_code == 201
    tokens = register_response.json()
    assert "access_token" in tokens
    
    # 2. Login User
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": user_email,
            "password": "strongpassword123"
        }
    )
    assert login_response.status_code == 200
    login_tokens = login_response.json()
    access_token = login_tokens["access_token"]
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 3. Get Me User info
    me_response = client.get("/api/v1/users/me", headers=headers)
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == user_email
    
    # 4. Get Dashboard Summary
    dashboard_response = client.get("/api/v1/dashboard/summary", headers=headers)
    assert dashboard_response.status_code == 200
    
    # 5. Get Today's agenda
    today_response = client.get("/api/v1/dashboard/today", headers=headers)
    assert today_response.status_code == 200
    
    # 6. Get identity profile
    identity_response = client.get("/api/v1/identity", headers=headers)
    assert identity_response.status_code == 200
    
    # 7. Get behavior profile
    behavior_response = client.get("/api/v1/behavior", headers=headers)
    assert behavior_response.status_code == 200
    
    # 8. Get missions
    missions_response = client.get("/api/v1/missions", headers=headers)
    assert missions_response.status_code == 200
    
    # 9. Get daily plan
    plan_response = client.get("/api/v1/planner/daily", headers=headers)
    assert plan_response.status_code == 200
    
    # 10. Get curator experience
    curator_response = client.get("/api/v1/curator", headers=headers)
    assert curator_response.status_code == 200
    
    # 11. Run Demo
    demo_response = client.post(
        "/api/v1/demo/run",
        headers=headers,
        json={"profile_name": "Student"}
    )
    assert demo_response.status_code == 200
    assert demo_response.json()["success"] is True
