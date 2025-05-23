# Electric Field Simulator

An interactive electric field simulator that allows users to visualize and manipulate electric fields created by point charges in a 2D space. The simulator provides real-time visualization of electric fields, 3D voltage plotting, and tools for measuring field strength at specific points.

## Features

- **Interactive Electric Field Visualization**: Real-time display of electric field lines and charge interactions
- **Dynamic Charge Manipulation**: Add, move, edit, and delete point charges in the simulation space
- **3D Voltage Plotting**: Visualize the voltage distribution in 3D using matplotlib
- **Test Point Functionality**: Measure electric field strength at any point in the simulation
- **Dual Polarity Support**: Create both positive and negative charges with different magnitudes
- **Real-time Field Updates**: Electric field visualization updates instantly as charges are moved

## Dependencies

- Python 3.x
- Pygame 2.6.1
- Matplotlib 3.9.0
- NumPy 2.0.0

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```

2. Install the required dependencies:
   ```bash
   pip install pygame matplotlib numpy
   ```

## Usage

Run the simulator by executing the main script:
```bash
python main.py
```

### Controls

- **i**: Enter Insert Mode (add new charges)
- **e**: Enter Edit Mode (modify existing charges)
- **ESC**: Return to Normal Mode
- **p**: Select positive charge polarity
- **n**: Select negative charge polarity
- **v**: Display 3D voltage plot
- **t**: Toggle charge polarity (in Edit Mode)
- **d**: Delete selected charge (in Edit Mode)
- **Left Mouse Button**: 
  - Insert Mode: Place new charge
  - Edit Mode: Select and drag charges

### Testing Electric Field

Click the "Test" button to spawn a test point at a random location. The simulator will display the electric field strength at that point.

## Technical Details

- Scale: 1 pixel = 1 cm in the simulation space
- Electric field calculations use Coulomb's law: F = k * q1 * q2 / r²
- Voltage calculations use V = k * q / r
- Charges are represented in nanocoulombs (nC)
- Electric field strength is displayed in Volts per meter (V/m)
- Coulomb's constant (k) = 8.988e9 N·m²/C²
