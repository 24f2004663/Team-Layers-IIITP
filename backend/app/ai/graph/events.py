from enum import Enum

class SystemEvent(str, Enum):
    """Event triggers driving the Life-GPS Agentic OS.
    
    Each event describes a specific system transition or lifecycle trigger,
    determining the activation sequence of specific agents.
    """

    APP_STARTED = "APP_STARTED"
    """Fires when the client app launches.
    
    First Agent Active: Identity Agent (to verify state, sync cache, and prepare session).
    """

    USER_LOGIN = "USER_LOGIN"
    """Fires immediately after a user successfully logs in.
    
    First Agent Active: Behavior Agent (to load user patterns and set current behavioral baseline).
    """

    USER_ONBOARDED = "USER_ONBOARDED"
    """Fires when a new user completes the onboarding process.
    
    First Agent Active: Identity Agent (to compile initial identity profile and generate seed values).
    """

    GOAL_UPDATED = "GOAL_UPDATED"
    """Fires when the user updates or creates a goal.
    
    First Agent Active: Planner Agent (to recalibrate the roadmap, set milestones, and update tasks).
    """

    HABIT_UPDATED = "HABIT_UPDATED"
    """Fires when a habit is ticked, edited, or reset.
    
    First Agent Active: Behavior Agent (to process current streak and update behavioral scores).
    """

    TASK_COMPLETED = "TASK_COMPLETED"
    """Fires when a planner task changes status to completed.
    
    First Agent Active: Reflection Agent (to analyze context and trigger immediate feedback loops).
    """

    RESOURCE_COMPLETED = "RESOURCE_COMPLETED"
    """Fires when the user completes a recommended reading, exercise, or video.
    
    First Agent Active: Curator Agent (to evaluate learning effectiveness and adjust recommendations).
    """

    REFLECTION_SUBMITTED = "REFLECTION_SUBMITTED"
    """Fires when the user submits their daily or weekly reflection log.
    
    First Agent Active: Reflection Agent (to synthesize inputs, identify cognitive blocks, and update profile).
    """

    DAY_STARTED = "DAY_STARTED"
    """Fires automatically when the user starts their day.
    
    First Agent Active: Planner Agent (to build the daily plan and present priority tasks).
    """

    DAY_ENDED = "DAY_ENDED"
    """Fires at the end of the user's active day.
    
    First Agent Active: Reflection Agent (to prompt user feedback and generate daily digest).
    """

    WEEK_STARTED = "WEEK_STARTED"
    """Fires on the first day of the week.
    
    First Agent Active: Planner Agent (to review goals and generate weekly roadmap).
    """

    WEEK_ENDED = "WEEK_ENDED"
    """Fires on the last day of the week.
    
    First Agent Active: Reflection Agent (to perform weekly review and output behavioral analysis).
    """

    MONTH_STARTED = "MONTH_STARTED"
    """Fires on the first day of the month.
    
    First Agent Active: Planner Agent (to plan monthly milestones and review long-term progress).
    """

    MONTH_ENDED = "MONTH_ENDED"
    """Fires on the last day of the month.
    
    First Agent Active: Reflection Agent (to generate comprehensive monthly growth report).
    """

    PROFILE_UPDATED = "PROFILE_UPDATED"
    """Fires when the user modifies personal details or core values.
    
    First Agent Active: Identity Agent (to update value alignments and personality profiles).
    """

    SYSTEM_SYNC = "SYSTEM_SYNC"
    """Fires periodically to sync backgrounds, clean memories, or archive sessions.
    
    First Agent Active: Orchestrator Agent (to run diagnostics and manage database alignment).
    """

    TASK_SKIPPED = "TASK_SKIPPED"
    RESOURCE_STARTED = "RESOURCE_STARTED"
    RESOURCE_ABANDONED = "RESOURCE_ABANDONED"
    SESSION_STARTED = "SESSION_STARTED"
    SESSION_ENDED = "SESSION_ENDED"
    MIDNIGHT_SYNC = "MIDNIGHT_SYNC"

