import 'package:life_gps/core/ai/ai_client.dart';
import 'package:life_gps/core/ai/agent_client.dart';
import 'package:life_gps/core/ai/streaming_client.dart';
import 'package:life_gps/core/ai/workflow_client.dart';
import 'package:mockito/mockito.dart';

class MockAiClient extends Mock implements AiClient {}

class MockWorkflowClient extends Mock implements WorkflowClient {}

class MockStreamingClient extends Mock implements StreamingClient {}

class MockAgentClient extends Mock implements AgentClient {}
