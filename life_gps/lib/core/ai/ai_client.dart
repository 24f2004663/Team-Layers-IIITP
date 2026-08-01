import 'agent_client.dart';
import 'streaming_client.dart';
import 'workflow_client.dart';

class AiClient {
  final WorkflowClient workflow;
  final StreamingClient streaming;
  final AgentClient agent;

  const AiClient({
    required this.workflow,
    required this.streaming,
    required this.agent,
  });
}
