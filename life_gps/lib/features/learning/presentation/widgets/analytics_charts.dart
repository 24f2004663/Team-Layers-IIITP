import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Renders a premium, animated line graph using CustomPainter.
class AnimatedLineChart extends StatefulWidget {
  final List<double> dataPoints;
  final Color lineColor;
  final Color fillColor;

  const AnimatedLineChart({
    super.key,
    required this.dataPoints,
    required this.lineColor,
    required this.fillColor,
  });

  @override
  State<AnimatedLineChart> createState() => _AnimatedLineChartState();
}

class _AnimatedLineChartState extends State<AnimatedLineChart>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    );
    _animation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOutCubic),
    );
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return CustomPaint(
          size: const Size(double.infinity, 160),
          painter: _LineChartPainter(
            dataPoints: widget.dataPoints,
            lineColor: widget.lineColor,
            fillColor: widget.fillColor,
            progress: _animation.value,
          ),
        );
      },
    );
  }
}

class _LineChartPainter extends CustomPainter {
  final List<double> dataPoints;
  final Color lineColor;
  final Color fillColor;
  final double progress;

  const _LineChartPainter({
    required this.dataPoints,
    required this.lineColor,
    required this.fillColor,
    required this.progress,
  });

  @override
  void paint(Canvas canvas, Size size) {
    if (dataPoints.isEmpty) return;

    final paint = Paint()
      ..color = lineColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3
      ..strokeCap = StrokeCap.round;

    final fillPaint = Paint()
      ..style = PaintingStyle.fill;

    final path = Path();
    final fillPath = Path();

    final double widthBetweenPoints = size.width / (dataPoints.length - 1);
    final double maxVal = dataPoints.reduce(math.max);
    final double minVal = dataPoints.reduce(math.min);
    final double range = (maxVal - minVal) == 0 ? 1.0 : (maxVal - minVal);

    double getX(int index) => index * widthBetweenPoints;
    double getY(double val) {
      final double normalized = (val - minVal) / range;
      // Subtract from size.height since canvas y-axis is inverted
      return size.height - (normalized * size.height * 0.8 * progress) - (size.height * 0.1);
    }

    path.moveTo(getX(0), getY(dataPoints[0]));
    fillPath.moveTo(getX(0), size.height);
    fillPath.lineTo(getX(0), getY(dataPoints[0]));

    for (int i = 1; i < dataPoints.length; i++) {
      final double currentX = getX(i);
      final double currentY = getY(dataPoints[i]);
      final double prevX = getX(i - 1);
      final double prevY = getY(dataPoints[i - 1]);

      // Control points for smooth bezier curves
      final double controlX1 = prevX + (currentX - prevX) / 2;
      final double controlY1 = prevY;
      final double controlX2 = prevX + (currentX - prevX) / 2;
      final double controlY2 = currentY;

      path.cubicTo(controlX1, controlY1, controlX2, controlY2, currentX, currentY);
      fillPath.cubicTo(controlX1, controlY1, controlX2, controlY2, currentX, currentY);
    }

    fillPath.lineTo(getX(dataPoints.length - 1), size.height);
    fillPath.close();

    // Create fill gradient
    final gradient = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [fillColor.withOpacity(0.3), fillColor.withOpacity(0.0)],
    );
    fillPaint.shader = gradient.createShader(Rect.fromLTWH(0, 0, size.width, size.height));

    canvas.drawPath(fillPath, fillPaint);
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant _LineChartPainter oldDelegate) {
    return oldDelegate.progress != progress || oldDelegate.dataPoints != dataPoints;
  }
}

/// Renders a beautiful Skill Radar Web Chart using CustomPainter.
class RadarSkillChart extends StatefulWidget {
  final Map<String, double> skills;
  final Color webColor;
  final Color fillColor;

  const RadarSkillChart({
    super.key,
    required this.skills,
    required this.webColor,
    required this.fillColor,
  });

  @override
  State<RadarSkillChart> createState() => _RadarSkillChartState();
}

class _RadarSkillChartState extends State<RadarSkillChart>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    );
    _animation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOutBack),
    );
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return CustomPaint(
          size: const Size(double.infinity, 220),
          painter: _RadarChartPainter(
            skills: widget.skills,
            webColor: widget.webColor,
            fillColor: widget.fillColor,
            progress: _animation.value,
          ),
        );
      },
    );
  }
}

class _RadarChartPainter extends CustomPainter {
  final Map<String, double> skills;
  final Color webColor;
  final Color fillColor;
  final double progress;

  const _RadarChartPainter({
    required this.skills,
    required this.webColor,
    required this.fillColor,
    required this.progress,
  });

  @override
  void paint(Canvas canvas, Size size) {
    if (skills.isEmpty) return;

    final center = Offset(size.width / 2, size.height / 2);
    final radius = math.min(size.width, size.height) / 2.8;

    final linePaint = Paint()
      ..color = webColor.withOpacity(0.2)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1;

    final fillPaint = Paint()
      ..color = fillColor.withOpacity(0.25)
      ..style = PaintingStyle.fill;

    final borderPaint = Paint()
      ..color = fillColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    final textPainter = TextPainter(
      textDirection: TextDirection.ltr,
    );

    final int vertexCount = skills.length;
    final double angleStep = (2 * math.pi) / vertexCount;

    // Draw background concentric web levels (3 grid circles)
    for (int step = 1; step <= 3; step++) {
      final double r = radius * (step / 3.0);
      final path = Path();
      for (int i = 0; i < vertexCount; i++) {
        final double angle = i * angleStep - math.pi / 2;
        final double x = center.dx + r * math.cos(angle);
        final double y = center.dy + r * math.sin(angle);
        if (i == 0) {
          path.moveTo(x, y);
        } else {
          path.lineTo(x, y);
        }
      }
      path.close();
      canvas.drawPath(path, linePaint);
    }

    // Draw spoke lines from center and axis labels
    final keys = skills.keys.toList();
    final values = skills.values.toList();

    for (int i = 0; i < vertexCount; i++) {
      final double angle = i * angleStep - math.pi / 2;
      final double x = center.dx + radius * math.cos(angle);
      final double y = center.dy + radius * math.sin(angle);

      // Draw spoke line
      canvas.drawLine(center, Offset(x, y), linePaint);

      // Draw text label
      final String label = keys[i].toUpperCase();
      textPainter.text = TextSpan(
        text: label,
        style: TextStyle(
          color: webColor,
          fontWeight: FontWeight.bold,
          fontSize: 9,
        ),
      );
      textPainter.layout();

      // Position label slightly outside the vertex
      final double labelX = center.dx + (radius + 20) * math.cos(angle) - (textPainter.width / 2);
      final double labelY = center.dy + (radius + 12) * math.sin(angle) - (textPainter.height / 2);
      textPainter.paint(canvas, Offset(labelX, labelY));
    }

    // Draw user skill fill polygon
    final path = Path();
    for (int i = 0; i < vertexCount; i++) {
      final double val = values[i] * progress;
      final double angle = i * angleStep - math.pi / 2;
      final double r = radius * val;
      final double x = center.dx + r * math.cos(angle);
      final double y = center.dy + r * math.sin(angle);

      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    path.close();

    canvas.drawPath(path, fillPaint);
    canvas.drawPath(path, borderPaint);
  }

  @override
  bool shouldRepaint(covariant _RadarChartPainter oldDelegate) {
    return oldDelegate.progress != progress || oldDelegate.skills != skills;
  }
}
