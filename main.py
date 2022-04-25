from ui import MathExpressionEvaluatorUi
from ui_bridge import BackendBridge
import tkinter as tk


if __name__ == "__main__":    
    backend_bridge = BackendBridge()
    root = tk.Tk()
    ui = MathExpressionEvaluatorUi(root, backend_bridge)
    
    ui.mainloop()

