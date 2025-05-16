# MoMo - Tool for Morphological Modeling 🧩

<div align="center">
<img src="resources/img/logo/logo_no_background.png" alt="MoMo Logo" width="400">
  <h3>Analysis and modeling of complex systems</h3>
</div>

---

## 📋 Table of Contents

* [About the Project](#-about-the-project)
* [Features](#-features)
* [Getting Started](#-getting-started)
* [Using the Program](#-using-the-program)
* [Project Structure](#-project-structure)
* [Technical Details](#-technical-details)

---

## 🔍 About the Project

**MoMo** (Morphological Modeling) is a powerful tool for morphological modeling and analysis of complex systems. The program allows you to create, import, and analyze systems with various characteristics, find optimal combinations of alternatives, and visualize results.

Morphological analysis is a method for structured exploration of the complete set of possible interrelationships in complex multidimensional problems. MoMo automates this process, making it accessible and intuitive.

---

## ✨ Features

* 📊 **System Creation**: Create systems with any number of characteristics and alternatives
* 📥 **Data Import**: Load systems from Excel files
* 🔄 **Morphological Modeling**: Automatically generate and analyze possible combinations
* 🎯 **Prototyping**: Create system prototypes and compare them with other combinations
* 📏 **Similarity Measures**: Use different similarity algorithms (Sorensen-Dice, Jaccard)
* 💾 **Export Results**: Save analysis results in Excel format
* 🤖 **AI Assistant**: Get help from the built-in AI assistant

---

## 🚀 Getting Started

### System Requirements

* Python 3.8+
* PyQt5
* pandas
* NumPy
* crewai (for the AI assistant)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/MoMoAna.git
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the program:

   ```
   python main.py
   ```

---

## 📖 Using the Program

### Main Window

The MoMo interface is divided into two main parts:

1. **Prototype Panel** (left) - for configuring the system prototype
2. **Systems/Results Panel** (right) - for working with systems and viewing results

### Creating a System

1. Click the ➕ **Add** button
2. Enter the system name
3. Add the required characteristics and alternatives

### Import from Excel

1. Click the 📥 **Load** button
2. Select an Excel file with data
3. The file should have characteristics in rows and alternatives in columns

### System Analysis

1. Set up the prototype on the left panel
2. Choose the similarity method (Sorensen-Dice or Jaccard)
3. Click **Calculate Combinations**
4. Results will appear in a new tab

### Using the AI Assistant

1. Click the **Ask AI** button in the bottom-right corner
2. Enter your question in the input field
3. The AI assistant will analyze the data and provide an answer

---

## 🏗️ Project Structure

```
MoMoAna/
├── main.py                  # Main entry point
├── gui/                     # Graphical user interface
│   ├── styles/              # Styling files
│   ├── widgets/             # UI widgets
│   └── windows/             # Application windows
├── src/                     # Core logic
│   ├── assistant/           # AI assistant
│   │   ├── core/            # Assistant core
│   │   ├── models/          # Data models
│   │   └── tools/           # Assistant tools
│   ├── dtypes/              # Data types
│   └── file_validator.py    # File validation
└── resources/               # Resources (images, icons)
```

---

## 🔧 Technical Details

### Similarity Measures

#### Sorensen-Dice

The Sorensen-Dice similarity coefficient is calculated as:

$\text{DSC} = \frac{2|A \cap B|}{|A| + |B|}$

where A and B are the sets being compared.

#### Jaccard

The Jaccard similarity coefficient is calculated as:

$J(A,B) = \frac{|A \cap B|}{|A \cup B|}$

### AI Assistant

The AI assistant uses CrewAI technology for data analysis and response generation. The assistant can:

* Explain results
* Recommend better combinations
* Help with data interpretation
* Answer questions about morphological modeling

---

<div align="center">
  <p>🌟 Developed with love for modeling and analysis 🌟</p>
  <p>© 2024 MoMo Team</p>
</div>
