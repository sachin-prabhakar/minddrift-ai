# MindDrift AI 🚀

**Collaborative Sci-Fi Story Writer**

MindDrift AI is an interactive Streamlit application that enables collaborative storytelling between humans and AI. Create captivating science fiction stories with customizable parameters for imagination, tone, surrealism, and emotional depth.


## ✨ Features

- **Collaborative Writing**: Alternate between AI-generated and human-written story parts
- **Customizable Parameters**: Fine-tune story generation with multiple sliders:
  - 🎨 **Imagination Level**: From realistic to hallucinatory
  - 🌙 **Tone**: From bright to nightmarish
  - 🌀 **Surrealism**: From grounded to unreal
  - 💫 **Emotional Charge**: From cold to gut-wrenching
  - ⚡ **Pace**: From introspective to relentless
  - 🔍 **Clarity**: Simple to complex language
- **Story Devices**: AI uses different narrative techniques for each part
- **Auto-Title Generation**: AI generates creative sci-fi titles
- **Export Options**: Download your stories as PDF or TXT files
- **Real-time Collaboration**: See your story develop part by part

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/minddrift-ai.git
   cd minddrift-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Or set the environment variable directly:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

4. **Run the application**
   ```bash
   streamlit run minddrift.py
   ```

5. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

## 🚀 Usage

### Getting Started

1. **Set Your Theme**: Enter a sci-fi story theme (e.g., "A detective discovers their memories are artificial")

2. **Adjust Parameters**: Use the sliders to customize the story's style:
   - Higher imagination = more creative and surreal content
   - Higher dark tone = darker, more ominous atmosphere
   - Higher surreal factor = more bizarre and dreamlike elements
   - Higher emotion = more intense emotional content
   - Higher pace = faster-paced action vs. introspective content

3. **Generate Story Parts**: 
   - Click "Generate AI Part" for AI-written sections
   - Write your own parts in the text areas for human sections
   - The AI uses different narrative devices for each part

4. **Refine Your Story**:
   - Use "Regenerate" to get different AI variations
   - Edit the title or let AI generate one automatically
   - View the prompts used to understand AI decisions

5. **Export Your Story**:
   - Download as PDF for formatted output
   - Download as TXT for plain text

### Story Structure

The app alternates between AI and human parts:
- **Part 1, 3, 5**: AI-generated with specific narrative devices
- **Part 2, 4**: Human-written sections

Each AI part uses a different storytelling technique:
- Dialogue between characters
- Flashbacks or memories
- Different perspectives
- Environmental descriptions
- Internal monologues
- News reports or data logs
- Questions and uncertainty
- Short, staccato sentences
- Twists and revelations
- Sensory details

## 🎛️ Parameters Guide

| Parameter | Low Value | High Value |
|-----------|-----------|------------|
| **Imagination** | Realistic, grounded | Hallucinatory, mind-bending |
| **Tone** | Bright, optimistic | Nightmarish, ominous |
| **Surreal** | Grounded, normal | Abstract, unreal |
| **Emotion** | Cold, reserved | Gut-wrenching, overwhelming |
| **Pace** | Introspective, slow | Relentless, explosive |
| **Clarity** | Simple language | Complex, poetic language |

## 🔧 Technical Details

- **Framework**: Streamlit
- **AI Model**: OpenAI GPT-3.5-turbo
- **PDF Generation**: FPDF
- **Text Processing**: Unicode normalization for clean output
- **Session Management**: Streamlit session state for story persistence

## 📁 Project Structure

```
minddrift-ai/
├── minddrift.py          # Main application file
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (not in repo)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

- You need a valid OpenAI API key to use this application
- API usage will incur costs based on OpenAI's pricing
- Keep your API key secure and never commit it to version control
- The app uses GPT-3.5-turbo for cost efficiency while maintaining quality

## 🆘 Troubleshooting

### Common Issues

1. **"Error generating content"**: Check your OpenAI API key and internet connection
2. **App won't start**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
3. **PDF download issues**: Check file permissions and available disk space

### Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your OpenAI API key is valid and has credits
3. Ensure all dependencies are correctly installed
4. Open an issue on GitHub with error details

## 🌟 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI](https://openai.com/)
- PDF generation with [FPDF](https://pyfpdf.readthedocs.io/)

---

**Happy storytelling! 📚✨** 