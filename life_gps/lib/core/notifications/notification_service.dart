class NotificationService {
  final List<String> notifications = [];

  void showLocalNotification({required String title, required String body}) {
    notifications.add('$title: $body');
  }

  void clearNotifications() {
    notifications.clear();
  }
}
