import tkinter as tk
import turtle
import json
import os
import random
import datetime

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
# tasks = [
#     {
#         "id": 1,
#         "title": "画一个边长为100的正方形",
#         "hint": "使用 for 循环重复4次，每次前进100然后右转90度",
#         "check": ["for", "forward(100)", "right(90)"]
#     },
#     {
#         "id": 2,
#         "title": "画一个半径为50的圆形",
#         "hint": "使用 pen.circle(50) 来画圆",
#         "check": ["circle(50)"]
#     },
#     {
#         "id": 3,
#         "title": "画一个五角星",
#         "hint": "重复5次，每次前进长度并右转144度",
#         "check": ["for", "right(144)"]
#     }
# ]

all_tasks = [
    {
        "id": "1",
        "title": "画一个边长为100的正方形",
        "hint": "使用 for 循环重复4次，每次前进100然后右转90度",
        "check": ["for", "forward(100)", "right(90)"]
    },
    {
        "id": "2",
        "title": "画一个半径为50的圆形",
        "hint": "使用 pen.circle(50) 来画圆",
        "check": ["circle(50)"]
    },
    {
        "id": "3",
        "title": "画一个五角星",
        "hint": "重复5次，每次前进长度并右转144度",
        "check": ["for", "right(144)"]
    },
    {
        "id": "4",
        "title": "画一个六边形",
        "hint": "使用 for 循环重复6次，每次前进并右转60度",
        "check": ["for", "right(60)"]
    },
    {
        "id": "5",
        "title": "画一个螺旋线",
        "hint": "使用 for 循环，每次前进距离递增并右转固定角度",
        "check": ["for", "forward", "right"]
    },
    {
        "id": "6",
        "title": "画一个平行四边形",
        "hint": "使用两个边长和角度组合，重复两次",
        "check": ["forward", "left"]
    },
    {
        "id": "7",
        "title": "画一个三角形",
        "hint": "使用 for 循环重复3次，每次前进并右转120度",
        "check": ["for", "right(120)"]
    },
    {
        "id": "8",
        "title": "画三个同心圆",
        "hint": "使用循环，每次画一个更大的圆",
        "check": ["for", "circle"]
    }
]
tasks = random.sample(all_tasks, 3)  # 随机选择3个任务


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

# def update_progress_display():
#     status = []
#     for task in tasks:
#         done = progress.get(str(task["id"]), False)
#         status.append(f"任务{task['id']}: {'✅已完成' if done else '❌未完成'}")
#     progress_display.config(state="normal")
#     progress_display.delete("1.0", tk.END)
#     progress_display.insert(tk.END, "\n".join(status))
#     progress_display.config(state="disabled")
def update_progress_display():
    status = []
    for task in tasks:
        task_id = str(task["id"])
        record = progress.get(task_id, {})

        # 如果旧记录是 bool 类型，转换成新结构
        if isinstance(record, bool):
            record = {
                "done": record,
                "timestamp": "",
                "attempts": 1 if record else 0
            }
            progress[task_id] = record  # 更新为新结构

        done = record.get("done", False)
        attempts = record.get("attempts", 0)
        timestamp = record.get("timestamp", "")
        title = task.get("title", f"任务 {task_id}")
        line = f"{title}: {'✅已完成' if done else '❌未完成'} | 操作次数: {attempts}"
        # if done and timestamp:
        #     try:
        #         from datetime import datetime
        #         t = datetime.fromisoformat(timestamp)
        #         line += f" | 完成时间: {t.strftime('%H:%M:%S')}"
        #     except:
        #         line += f" | 完成时间: {timestamp}"
        status.append(line)

    progress_display.config(state="normal")
    progress_display.delete("1.0", tk.END)
    progress_display.insert(tk.END, "\n".join(status))
    progress_display.config(state="disabled")


# ------------------ 图形绘制函数 ------------------
def draw_hexagon():
    reset_screen()
    try:
        length = int(param_entry.get() or 100)
    except ValueError:
        show_code("请输入有效的整数参数")
        return
    pen = turtle.Turtle()
    for _ in range(6):
        pen.forward(length)
        pen.right(60)
    pen.hideturtle()
    show_code(f"pen = turtle.Turtle()\nfor _ in range(6):\n    pen.forward({length})\n    pen.right(60)\npen.hideturtle()")

def draw_concentric_circles():
    reset_screen()
    try:
        radius = int(param_entry.get() or 30)
    except ValueError:
        show_code("请输入有效的整数参数")
        return
    radius = 30
    pen = turtle.Turtle()
    pen.up()
    for i in range(3):
        pen.goto(0, -radius * (i + 1))
        pen.down()
        pen.circle(radius * (i + 1))
        pen.up()
    pen.hideturtle()
    show_code(
        "radius = 30\npen = turtle.Turtle()\npen.up()\nfor i in range(3):\n    pen.goto(0, -radius*(i+1))\n    pen.down()\n    pen.circle(radius*(i+1))\n    pen.up()\npen.hideturtle()"
    )

def draw_spiral():
    reset_screen()
    pen = turtle.Turtle()
    for i in range(50):
        pen.forward(i * 2)
        pen.right(45)
    pen.hideturtle()
    show_code(
        "pen = turtle.Turtle()\nfor i in range(50):\n    pen.forward(i * 2)\n    pen.right(45)\npen.hideturtle()"
    )


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
        task_id = str(task["id"])
        if task_id not in progress or not isinstance(progress[task_id], dict):
            progress[task_id] = {"done": False, "timestamp": "", "attempts": 0}

        progress[task_id]["attempts"] += 1

        if check_code(user_code, task["check"]):
            progress[task_id]["done"] = True
            progress[task_id]["timestamp"] = datetime.datetime.now().isoformat()
            save_progress(progress)
            show_code(user_code)

            # 自动跳转到下一个任务
            current_index = tasks.index(task)
            if current_index + 1 < len(tasks):
                feedback_label.config(text="✅ 太棒了！你完成了这个任务！已进入下一个任务 👇")
                show_task(current_index + 1)
            else:
                feedback_label.config(text="🎉 所有任务已完成！你可以点击『刷新任务池』再挑战一次！")
        else:
            feedback_label.config(text="⚠️ 图形绘制成功，但代码结构不完全符合任务要求")
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

# btn_square = tk.Button(root, text="画正方形", command=draw_square)
# btn_square.pack(pady=2)

# btn_triangle = tk.Button(root, text="画三角形", command=draw_triangle)
# btn_triangle.pack(pady=2)

# btn_circle = tk.Button(root, text="画圆形", command=draw_circle)
# btn_circle.pack(pady=2)

# btn_star = tk.Button(root, text="画五角星", command=draw_star)
# btn_star.pack(pady=2)

# btn_clear = tk.Button(root, text="清空画布", fg="red", command=clear_canvas)
# btn_clear.pack(pady=5)

# btn_hexagon = tk.Button(root, text="画六边形", command=draw_hexagon)
# btn_hexagon.pack(pady=2)

# btn_concentric = tk.Button(root, text="画同心圆", command=draw_concentric_circles)
# btn_concentric.pack(pady=2)

# btn_spiral = tk.Button(root, text="画螺旋线", command=draw_spiral)
# btn_spiral.pack(pady=2)

# 创建一个新的按钮容器
shape_buttons_frame = tk.Frame(root)
shape_buttons_frame.pack(pady=10)

# 平行四边形
def draw_parallelogram():
    reset_screen()
    try:
        length = int(param_entry.get() or 100)
        width = int(length * 0.6)  # 可以自定义比例
        angle = 60  # 平行四边形的锐角
    except ValueError:
        show_code("请输入有效的整数参数")
        return
    pen = turtle.Turtle()
    for _ in range(2):
        pen.forward(length)
        pen.left(angle)
        pen.forward(width)
        pen.left(180 - angle)
    pen.hideturtle()
    show_code(
        f"pen = turtle.Turtle()\nfor _ in range(2):\n    pen.forward({length})\n    pen.left({angle})\n    pen.forward({width})\n    pen.left({180 - angle})\npen.hideturtle()"
    )


# 按钮列表和对应函数
shape_buttons = [
    ("画正方形", draw_square),
    ("画三角形", draw_triangle),
    ("画圆形", draw_circle),
    ("画五角星", draw_star),
    ("画平行四边形", draw_parallelogram),  # 这里暂时用画正方形的函数代替
    ("画六边形", draw_hexagon),
    ("画同心圆", draw_concentric_circles),
    ("画螺旋线", draw_spiral),
    ("清空画布", clear_canvas, "red")
]

# 使用 grid 排列成 2 行 × 4 列
for i, item in enumerate(shape_buttons):
    if len(item) == 3:
        label, func, color = item
        btn = tk.Button(shape_buttons_frame, text=label, width=12, fg=color, command=func)
    else:
        label, func = item
        btn = tk.Button(shape_buttons_frame, text=label, width=12, command=func)
    btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)




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

# task_buttons_frame = tk.Frame(root)
# task_buttons_frame.pack(pady=5)
# for i in range(len(tasks)):
#     btn = tk.Button(task_buttons_frame, text=f"任务{i+1}", command=lambda i=i: show_task(i))
#     btn.grid(row=0, column=i, padx=5)
def refresh_tasks():
    global tasks
    tasks = random.sample(all_tasks, 3)
    show_task(0)

#学习报告导出功能

def generate_learning_report():
    total = len(tasks)
    completed = 0
    most_attempts = ("", 0)
    recent_task = ("", "")

    lines = ["📘 学习报告", "------------------"]
    for task in tasks:
        task_id = str(task["id"])
        title = task.get("title", task_id)
        record = progress.get(task_id, {})
        if isinstance(record, bool):
            record = {"done": record, "timestamp": "", "attempts": 1 if record else 0}
        done = record.get("done", False)
        attempts = record.get("attempts", 0)
        timestamp = record.get("timestamp", "")
        if done:
            completed += 1
            if timestamp > recent_task[1]:
                recent_task = (title, timestamp)
        if attempts > most_attempts[1]:
            most_attempts = (title, attempts)
        line = f"{title}: {'✅已完成' if done else '❌未完成'} | 操作次数: {attempts}"
        if done and timestamp:
            line += f" | 完成时间: {timestamp.split('T')[1][:8]}"
        lines.append(line)

    lines.append("------------------")
    lines.append(f"总任务数: {total}")
    lines.append(f"已完成任务: {completed}")
    lines.append(f"完成率: {round(completed / total * 100, 1)}%")
    lines.append(f"最近完成任务: {recent_task[0]} 于 {recent_task[1].split('T')[1][:8]}" if recent_task[1] else "最近完成任务: 无")
    lines.append(f"最多操作任务: {most_attempts[0]}（{most_attempts[1]} 次）")

    return "\n".join(lines)

    generate_learning_report()

# task_buttons_frame = tk.Frame(root)
# task_buttons_frame.pack(pady=5)



# refresh_btn = tk.Button(task_buttons_frame, text="🔄 刷新任务池", fg="blue", command=refresh_tasks)
# refresh_btn.pack()

# report_btn = tk.Button(root, text="📊 生成学习报告", command=generate_learning_report)
# report_btn.pack(pady=5)

# report_display = tk.Text(root, height=12, width=60, bg="#f9f9f9")
# report_display.pack(pady=5)
# report_display.config(state="disabled")

def show_report_popup():
    report_window = tk.Toplevel(root)
    report_window.title("📊 学习报告")
    report_window.geometry("500x400")

    report_text = tk.Text(report_window, wrap="word", bg="#f9f9f9", font=("Arial", 10))
    report_text.pack(expand=True, fill="both", padx=10, pady=10)

    report_text.insert(tk.END, generate_learning_report())
    report_text.config(state="disabled")


# 创建横向按钮容器
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# 刷新任务池按钮
refresh_btn = tk.Button(button_frame, text="🔄 刷新任务池", command=refresh_tasks)
refresh_btn.pack(side="left", padx=10)

# 生成学习报告按钮
report_btn = tk.Button(button_frame, text="📊 生成学习报告", command=show_report_popup)
report_btn.pack(side="left", padx=10)





show_task(0)

root.mainloop()
