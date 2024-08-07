# Game Project

## Setup and Run Instructions

1. Clone the Repository
First, clone the repository to your local machine using the following command:

```bash
git clone <https://github.com/LukasJanusk/CAPSTONE1>
```

2. Navigate to the Project Directory
Change your current directory to the project directory:
```bash
cd <CAPSTONE1>
```
3. Install Dependencies

Ensure you have Python installed. It's recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment with:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Run game
```bash
python run_game.py
```

## Controls

### Menu Controls
- **Navigate Up**: `W` or `Up Arrow`
- **Navigate Down**: `S` or `Down Arrow`
- **Select/Confirm**: `Enter`

### In-Game Controls
- **Jump**: `W`
- **Duck**: `S` (currently does nothing)
- **Move Left**: `A`
- **Move Right**: `D`
- **Hold to Run**: `LShift` (currently no animation)
- **Hold to Charge and Execute Heavy Attack**: `Y`
- **Quick Combo Attack**: `U` (hold to repeat continuously)
- **Hold to Block**: `Space`
- **Pause Game**: `Esc`


## Project Structure

CAPSTONE1/
├── assets/
│ ├── sounds/
│ ├── musics/
│ ├── graphics/
│ │ ├── levels/
│ │ └── sprites/
│ └── fonts/
├── docs/
│ ├── design.md
│ ├── user_manual.md
│ └── developer_guide.md
├── game/
├── tests/
├── user/
│ ├── profiles/
│ └── settings/
├── run_game.py
├── TODO.txt
├── requirements.txt
└── README.md