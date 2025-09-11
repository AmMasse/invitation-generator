# Template-Based Invitation Generator

A professional desktop application for creating personalized invitations with custom templates.

## Features

- 🎨 **Custom Templates**: Upload your own designed backgrounds (PNG/JPG)
- 📐 **Precise Positioning**: Millimeter-accurate text placement
- 📊 **Batch Processing**: Generate hundreds of invitations from Excel data
- 🖨️ **Print Ready**: Professional A5 PDF output (148×210mm)
- 🔗 **Interactive RSVPs**: Clickable buttons with personalized links
- 💻 **Cross Platform**: Windows, macOS, and Linux support

## Quick Start

### Download Pre-built Executable
1. Go to [Releases](../../releases)
2. Download the version for your operating system:
   - **Windows**: `InvitationGenerator-Windows.exe`
   - **macOS**: `InvitationGenerator-macOS`
   - **Linux**: `InvitationGenerator-Linux`
3. Run the executable (no installation required)

### From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/invitation-generator.git
cd invitation-generator

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## How to Use

### 1. Design Your Template
Create a beautiful background design using:
- Photoshop, Canva, or any design tool
- Recommended size: A5 (148×210mm) or 1754×2480 pixels
- Leave space for text elements (name, message, details, button)
- Save as PNG or JPG

### 2. Prepare Your Data
Create an Excel file (.xlsx) with these exact columns:
```
Name          | Link                           | Occasion
John Smith    | https://rsvp.com/wedding/john  | Wedding Reception
Sarah Johnson | https://rsvp.com/wedding/sarah | Wedding Reception
Mike Wilson   | https://rsvp.com/party/mike    | Birthday Party
```

### 3. Generate Invitations
1. **Select Template**: Upload your background image
2. **Position Text**: Set precise coordinates (in millimeters) for:
   - Guest names
   - Main message
   - Event details
   - RSVP button
3. **Load Data**: Choose your Excel file
4. **Generate**: Create personalized PDFs for each guest

## Text Positioning Guide

The app uses millimeter coordinates from the bottom-left corner:

```
A5 Page (148×210mm)
┌─────────────────────┐ 210mm
│ Header Area         │
│ (name: ~170mm)      │
├─────────────────────┤
│ Message Area        │
│ (message: ~150mm)   │
├─────────────────────┤
│ Details Area        │
│ (details: ~120mm)   │
├─────────────────────┤
│ Button Area         │
│ (button: ~40mm)     │
└─────────────────────┘ 0mm
0mm                148mm
```

## Template Design Tips

- **Safe Margins**: Keep important design elements 10mm from edges
- **Text Zones**: Design with text placement in mind
- **High Resolution**: Use 300 DPI for print quality
- **Color Mode**: RGB for screen, CMYK if printing professionally
- **File Size**: Keep under 50MB for best performance

## Building from Source

### Prerequisites
- Python 3.11+
- Git

### Build Executable
```bash
# Install build dependencies
pip install pyinstaller

# Build for your platform
pyinstaller invitation_generator.spec

# Find executable in dist/ folder
```

### Automated Builds
This repository uses GitHub Actions to automatically build executables for all platforms when you:
1. Push code to main branch
2. Create a release tag (e.g., `v1.0.0`)

## Troubleshooting

### Common Issues

**Template not loading:**
- Ensure image is PNG/JPG format
- Check file size (under 50MB recommended)
- Try converting RGBA to RGB

**Text positioning off:**
- Remember coordinates are from bottom-left
- Use preview feature to test positioning
- Adjust coordinates in small increments (1-2mm)

**Excel file errors:**
- Ensure exact column names: Name, Link, Occasion
- Remove empty rows
- Save as .xlsx format (not .xls)

### Getting Help
- Check the [Issues](../../issues) page
- Create a new issue with:
  - Your operating system
  - Error message (if any)
  - Screenshots of the problem

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you find this tool useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📖 Improving documentation