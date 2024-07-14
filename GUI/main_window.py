import tkinter as tk


def draw_separator(canvas, x1, y1, x2, y2, color):
    canvas.create_line(x1, y1, x2, y2, fill=color, width=2)


def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("主界面示例")

    # 设置窗口大小
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    # 创建一个主框架，用于放置其他组件
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 创建侧边栏和主界面内容区域
    sidebar = tk.Frame(main_frame)
    content_area = tk.Frame(main_frame)

    # 将侧边栏和内容区的列位置互换
    content_area.grid(row=0, column=0, sticky="nsew")
    sidebar.grid(row=0, column=1, sticky="ns")

    # 创建下边栏
    bottom_bar = tk.Frame(main_frame)
    bottom_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    # 创建一个用于绘制分隔线的Canvas
    canvas = tk.Canvas(main_frame, bg="white")
    canvas.grid(row=0, column=0, sticky="nsew")

    # 调整列权重，使得主界面内容区域比侧边栏宽
    main_frame.columnconfigure(0, weight=4)  # 主界面内容区域占80%
    main_frame.columnconfigure(1, weight=1)  # 侧边栏占20%
    main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
    main_frame.rowconfigure(1, minsize=200)  # 下边栏有最小高度100像素

    # 绘制分隔线
    sidebar_width = sidebar.winfo_reqwidth()
    content_area_width = content_area.winfo_reqwidth()
    screen_height = root.winfo_screenheight()

    # 分割线现在应该从内容区的右边界画到屏幕底部
    draw_separator(canvas, screen_width - sidebar_width, 0, screen_width - sidebar_width, screen_height - 100, "black")
    draw_separator(canvas, 0, screen_height - 100, screen_width, screen_height - 100, "black")

    # 在侧边栏添加一些内容
    tk.Label(sidebar, text="侧边栏").pack(expand=True, fill='both')

    # 在下边栏添加一些内容
    tk.Label(bottom_bar, text="下边栏").pack(fill='x')

    # 在主界面内容区域添加一些内容
    tk.Label(content_area, text="主界面").pack(expand=True, fill='both')

    # 运行事件循环
    root.mainloop()


if __name__ == "__main__":
    main()