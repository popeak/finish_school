import tkinter as tk
import turtle
import json
import os

# ------------------ Turtle 初始化 ------------------
screen = turtle.Screen()
screen.title("儿童编程学习平台")

def reset_screen():
    global screen
    try:
        screen.clearscreen()
    except turtle.Terminator:
        screen = turtle.Screen()
        screen.title("儿童编程学习平台")

def show_code(code_text):
    code_display.config(state="normal")
    code_display.delete("1.0", tk.END)
    code_display.insert(tk.END, code_text)
    code_display.config(state="disabled")

# ------------------ 任务系统 ------------------
tasks = [
    {
        "id": 1,
        "title": "画一个边长为100的正方形",
        "hint": "使用 for 循环重复4次，每次前进100然后右转90度",
        "check": ["for", "forward(100)", "right(90)"]
    },
    {
        "id": 2,
        "title": "画一个半径为50的圆形",
        "hint": "使用 pen.circle(50) 来画圆",
        "check": ["circle(50)"]
    },
    {
        "id": 3,
        "title": "画一个五角星",
        "hint": "重复5次，每次前进长度并右转144度",
        "check": ["for", "right(144)"]
    }
]

progress_file = "progress.json"

def load_progress():
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(progress_file, "w") as f:
        json.dump(progress, f)

progress = load_progress()

def check_code(code, keywords):
    return all(kw in code for kw in keywords)

def update_progress_display():
    status = []
    for task in tasks:
        done = progress.get(str(task["id"]), False)
        status.append(f"任务{task['id']}: {'✅已完成' if done else '❌未完成'}")
    progress_display.config(state="normal")
    progress_display.delete("1.0", tk.END)
    progress_display.insert(tk.END, "\n".join(status))
    progress_display.config(state="disabled")

# ------------------ 图形绘制函数 ------------------
def draw_square():
    reset_screen()
    try:
        length = int(param_entry.get() or 100)
    except ValueError:
        show_code("请输入有效的整数参数")
        return
    pen = turtle.Turtle()
    for _ in range(4):
        pen.forward(length)
        pen.right(90)
    pen.hideturtle()
    show_code(f"pen = turtle.Turtle()\nfor _ in range(4):\n    pen.forward({length})\n    pen.right(90)\npen.hideturtle()")

def draw_triangle():
    reset_screen()
    try:
        length = int(param_entry.get() or 100)
    except ValueError:
        show_code("请输入有效的整数参数")
        return
    pen = turtle.Turtle()
    for _ in range(3):
        pen.forward(length)
        pen.right(120)
    pen.hideturtle()
    show_code(f"pen = turtle.Turtle()\nfor _ in range(3):\n    pen.forward({length})\n    pen.right(120)\npen.hideturtle()")

def draw_circle():
    reset_screen()
    try:
        radius = int(param_entry.get() or 50)
    except ValueError:
        show_code("请输入有效的整数参数")
        return
    pen = turtle.Turtle()
    pen.circle(radius)
    pen.hideturtle()
    show_code(f"pen = turtle.Turtle()\npen.circle({radius})\npen.hideturtle()")

def draw_star():
    reset_screen()
    try:
        length = int(param_entry.get() or 100)
    except ValueError:
        show_code("请输入有效的整数参数")
        return
    pen = turtle.Turtle()
    for _ in range(5):
        pen.forward(length)
        pen.right(144)
    pen.hideturtle()
    show_code(f"pen = turtle.Turtle()\nfor _ in range(5):\n    pen.forward({length})\n    pen.right(144)\npen.hideturtle()")

def clear_canvas():
    reset_screen()
    show_code("画布已清空")

# ------------------ 教学任务功能 ------------------
def show_task(index):
    task = tasks[index]
    task_label.config(text=f"任务 {task['id']}: {task['title']}")
    hint_button.config(command=lambda: feedback_label.config(text=f"提示：{task['hint']}"))
    run_button.config(command=lambda: run_custom_code(task))
    code_input.delete("1.0", tk.END)
    feedback_label.config(text="")
    update_progress_display()

def run_custom_code(task=None):
    reset_screen()
    user_code = code_input.get("1.0", tk.END)
    try:
        exec(user_code, {"turtle": turtle})
        if task:
            if check_code(user_code, task["check"]):
                feedback_label.config(text="✅ 太棒了！你完成了这个任务！")
                progress[str(task["id"])] = True
                save_progress(progress)
            else:
                feedback_label.config(text="⚠️ 图形绘制成功，但代码结构不完全符合任务要求")
        else:
            feedback_label.config(text="✅ 代码运行成功")
        show_code(user_code)
    except Exception as e:
        feedback_label.config(text=f"❌ 错误：{e}")
        show_code(f"错误：{e}")
    update_progress_display()

# ------------------ Tkinter UI ------------------
root = tk.Tk()
root.title("儿童编程教学平台")

param_label = tk.Label(root, text="参数（长度/半径）：")
param_label.pack()
param_entry = tk.Entry(root)
param_entry.pack()

btn_square = tk.Button(root, text="画正方形", command=draw_square)
btn_square.pack(pady=2)

btn_triangle = tk.Button(root, text="画三角形", command=draw_triangle)
btn_triangle.pack(pady=2)

btn_circle = tk.Button(root, text="画圆形", command=draw_circle)
btn_circle.pack(pady=2)

btn_star = tk.Button(root, text="画五角星", command=draw_star)
btn_star.pack(pady=2)

btn_clear = tk.Button(root, text="清空画布", fg="red", command=clear_canvas)
btn_clear.pack(pady=5)

code_label = tk.Label(root, text="请输入 Turtle 代码：")
code_label.pack()
code_input = tk.Text(root, height=6, width=50)
code_input.pack()

run_button = tk.Button(root, text="运行代码", fg="blue")
run_button.pack(pady=5)

task_label = tk.Label(root, text="当前任务：", font=("Arial", 12))
task_label.pack(pady=5)

hint_button = tk.Button(root, text="显示提示", fg="purple")
hint_button.pack(pady=2)

feedback_label = tk.Label(root, text="", fg="green", wraplength=400)
feedback_label.pack(pady=5)

progress_display = tk.Text(root, height=5, width=50, bg="#f0f0f0")
progress_display.pack(pady=10)
progress_display.config(state="disabled")

code_display = tk.Text(root, height=6, width=50, bg="#f0f0f0")
code_display.pack(pady=10)
code_display.config(state="disabled")

task_buttons_frame = tk.Frame(root)
task_buttons_frame.pack(pady=5)
for i in range(len(tasks)):
    btn = tk.Button(task_buttons_frame, text=f"任务{i+1}", command=lambda i=i: show_task(i))
    btn.grid(row=0, column=i, padx=5)

show_task(0)

root.mainloop()
