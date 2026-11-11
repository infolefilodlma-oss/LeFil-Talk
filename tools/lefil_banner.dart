// SPDX-License-Identifier: AGPL-3.0-or-later
// Bandeau propre a Le Fil Talk : aucun changement des fonctions Matrix.
import 'package:material_ui/material_ui.dart';
import 'package:url_launcher/url_launcher_string.dart';

class LeFilBanner extends StatelessWidget {
  final bool compact;
  const LeFilBanner({super.key, this.compact = false});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: compact ? 72 : 76,
      width: double.infinity,
      child: Stack(
        fit: StackFit.expand,
        children: [
          const DecoratedBox(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  Color(0xFF190B4C),
                  Color(0xFF0B041B),
                  Color(0xFF4900BA),
                ],
                stops: [0.0, 0.48, 1.0],
              ),
            ),
          ),
          const CustomPaint(painter: _LeFilWavePainter()),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
            child: Row(
              children: [
                Image.asset(
                  './assets/logo/mini/logo_mini.png',
                  width: compact ? 48 : 54,
                  height: compact ? 48 : 54,
                  fit: BoxFit.contain,
                ),
                const Spacer(),
                TextButton.icon(
                  onPressed: () => launchUrlString(
                    'https://le-fil.net/',
                    mode: LaunchMode.externalApplication,
                  ),
                  icon: const Icon(Icons.arrow_back, size: 17),
                  label: const Text(
                    'Accueil du Fil',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  style: TextButton.styleFrom(
                    foregroundColor: Colors.white,
                    backgroundColor: const Color(0x995D32B9),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 9,
                      vertical: 8,
                    ),
                    shape: const StadiumBorder(),
                    textStyle: TextStyle(
                      fontFamily: 'Poppins',
                      fontSize: compact ? 12 : 13,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _LeFilWavePainter extends CustomPainter {
  const _LeFilWavePainter();

  @override
  void paint(Canvas canvas, Size size) {
    final wave = Path()
      ..moveTo(0, size.height * 0.38)
      ..cubicTo(
        size.width * 0.22, size.height * 0.73,
        size.width * 0.38, size.height * 0.95,
        size.width * 0.59, size.height * 0.48,
      )
      ..cubicTo(
        size.width * 0.77, size.height * 0.03,
        size.width * 0.90, size.height * 0.10,
        size.width, 0,
      )
      ..lineTo(size.width, size.height)
      ..lineTo(0, size.height)
      ..close();
    final paint = Paint()
      ..shader = const LinearGradient(
        begin: Alignment.bottomLeft,
        end: Alignment.topRight,
        colors: [
          Color(0xFFF128AC),
          Color(0xFF7400D7),
          Color(0xFF3900A6),
        ],
      ).createShader(Offset.zero & size);
    canvas.drawPath(wave, paint);
  }

  @override
  bool shouldRepaint(covariant _LeFilWavePainter oldDelegate) => false;
}
