import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final bool isFullWidth;
  final ButtonType type;
  final IconData? icon;

  const CustomButton({
    Key? key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.isFullWidth = true,
    this.type = ButtonType.primary,
    this.icon,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Widget child = isLoading
        ? const SizedBox(
            height: 20,
            width: 20,
            child: CircularProgressIndicator(
              strokeWidth: 2,
              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
            ),
          )
        : Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (icon != null) ...[
                Icon(icon, size: 18),
                const SizedBox(width: 8),
              ],
              Text(
                text,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: _getTextColor(),
                ),
              ),
            ],
          );

    Widget button = ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: _getBackgroundColor(),
        foregroundColor: _getTextColor(),
        elevation: type == ButtonType.primary ? 2 : 0,
        shadowColor: Colors.black26,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: type == ButtonType.secondary
              ? BorderSide(color: Colors.grey[300]!)
              : BorderSide.none,
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: 24,
          vertical: 16,
        ),
        minimumSize: isFullWidth ? const Size(double.infinity, 52) : null,
      ),
      child: child,
    );

    return button;
  }

  Color _getBackgroundColor() {
    switch (type) {
      case ButtonType.primary:
        return const Color(0xFF3B82F6); // Blue
      case ButtonType.secondary:
        return Colors.white;
      case ButtonType.danger:
        return const Color(0xFFEF4444); // Red
    }
  }

  Color _getTextColor() {
    switch (type) {
      case ButtonType.primary:
      case ButtonType.danger:
        return Colors.white;
      case ButtonType.secondary:
        return const Color(0xFF374151); // Gray
    }
  }
}

enum ButtonType {
  primary,
  secondary,
  danger,
}
