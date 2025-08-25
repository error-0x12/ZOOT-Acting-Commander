import tkinter as tk
from tkinter import ttk, font, messagebox, scrolledtext
import os
import sys
import time
import logging

# 将项目根目录添加到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils import logger
from modules import BaseManagementModule, CombatModule, TaskManagementModule
from core.exceptions import ElementNotFoundError, OperationFailedError
from config.settings import settings

class ZOOTGui:
    def __init__(self, root):
        # 设置主窗口
        self.root = root
        self.root.title("ZOOT Acting Commander")
        self.root.geometry("1365x768+100+100")
        self.root.overrideredirect(True)  # 无边框
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  # 窗口置顶
        
        # 窗口拖动相关变量
        self.x = 0
        self.y = 0
        
        # 背景图片路径（预留）
        self.background_image_path = os.path.join(os.path.dirname(__file__), "../templates/background.png")
        
        # 标题图片路径（预留）
        self.title_image_path = os.path.join(os.path.dirname(__file__), "icon", "title-ZOOT-white.png")
        
        # 初始化模块实例（避免重复初始化）
        self.base_manager = BaseManagementModule()
        self.combat_manager = CombatModule()
        self.task_manager = TaskManagementModule()
        
        # 初始化日志窗口
        self.init_log_window()
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题栏（用于拖动窗口）
        self.title_bar = tk.Frame(self.main_frame, bg="#2d2d2d", height=30)
        self.title_bar.pack(side=tk.TOP, fill=tk.X)
        
        # 添加标题栏拖动功能
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)
        
        # 创建标题栏标题（文字显示）
        self.title_label = tk.Label(
            self.title_bar, 
            text="ZOOT Acting Commander", 
            font=font.Font(family="SimHei", size=10, weight="bold"),
            bg="#2d2d2d", 
            fg="#ffffff"
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # 创建侧边栏
        self.sidebar = tk.Frame(self.main_frame, width=180, bg="#2d2d2d")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # 创建侧边栏标题（使用图片）
        try:
            # 尝试加载标题图片
            self.sidebar_title_image = tk.PhotoImage(file=self.title_image_path)
            self.title_label = tk.Label(
                self.sidebar, 
                image=self.sidebar_title_image, 
                bg="#2d2d2d",
                pady=15
            )
        except Exception as e:
            print(f"加载侧边栏标题图片失败: {e}")
            # 如果加载失败，使用文字替代
            self.title_label = tk.Label(
                self.sidebar, 
                text="ZOOT Acting Commander", 
                font=font.Font(family="SimHei", size=12, weight="bold"),
                bg="#2d2d2d", 
                fg="#ffffff",
                pady=15
            )
        self.title_label.pack()
        
        # 创建侧边栏标签按钮
        self.tabs = [
            {"text": "主页", "icon": "home_btn.png", "command": self.show_home},
            {"text": "任务管理", "icon": "main_task_btn.png", "command": self.show_task_management},
            {"text": "基建管理", "icon": "main_menu_base_btn.png", "command": self.show_base_management},
            {"text": "作战管理", "icon": "combat_briefing.png", "command": self.show_combat},
            {"text": "招募管理", "icon": "main_recruit_button.png", "command": self.show_recruit},
            {"text": "配置", "icon": "settings.png", "command": self.show_settings},
            {"text": "关于", "icon": "about.png", "command": self.show_about}
        ]
        
        self.tab_buttons = []
        for tab in self.tabs:
            btn = tk.Button(
                self.sidebar, 
                text=tab["text"],
                font=font.Font(family="SimHei", size=10),
                bg="#2d2d2d", 
                fg="#cccccc",
                bd=0,
                padx=10,
                pady=10,
                anchor="w",
                command=tab["command"]
            )
            btn.pack(fill=tk.X)
            self.tab_buttons.append(btn)
            
            # 鼠标悬停效果
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3d3d3d", fg="#ffffff"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2d2d2d", fg="#cccccc"))
        
        # 创建内容区域
        self.content_area = tk.Frame(self.main_frame, bg="#1a1a1a")
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 创建关闭按钮
        self.close_button = tk.Label(
            self.title_bar,
            text="✕",
            font=font.Font(family="SimHei", size=12, weight="bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        self.close_button.pack(side=tk.RIGHT, padx=10)
        self.close_button.bind("<Button-1>", lambda e: self.on_closing())
        
        # 记录当前截图存储设置状态
        logger.info(f"程序启动，当前截图存储设置: {'启用' if settings.SAVE_SCREENSHOTS else '禁用'}")
        
        # 显示主页
        self.show_home()
        
    def show_home(self):
        self.clear_content_area()
        title = tk.Label(
            self.content_area, 
            text="Welcome to ZOOT Acting Commander\n\n欢迎使用 ZOOT 代理指挥系统", 
            font=font.Font(family="SimHei", size=20, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        title.pack(pady=50)
        
        desc = tk.Label(
            self.content_area, 
            text="让游戏更简单", 
            font=font.Font(family="SimHei", size=12),
            bg="#1a1a1a", 
            fg="#cccccc",
            justify=tk.CENTER
        )
        desc.pack()
        
    def show_task_management(self):
        self.clear_content_area()
        title = tk.Label(
            self.content_area, 
            text="任务管理", 
            font=font.Font(family="SimHei", size=16, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        title.pack(pady=20)
        
        # 此处添加任务管理相关控件
        test_btn = tk.Button(
            self.content_area, 
            text="领取任务奖励(日常以及周常)", 
            font=font.Font(family="SimHei", size=10),
            bg="#3d3d3d", 
            fg="#ffffff",
            bd=0,
            padx=10,
            pady=5,
            command=self.claim_task_rewards
        )
        test_btn.pack(pady=10)
        
    def show_base_management(self):
        self.clear_content_area()
        title = tk.Label(
            self.content_area, 
            text="基建管理", 
            font=font.Font(family="SimHei", size=16, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        title.pack(pady=20)
        
        # 创建完成基建事项按钮
        complete_tasks_btn = tk.Button(
            self.content_area, 
            text="完成基建事项", 
            font=font.Font(family="SimHei", size=12),
            bg="#3d3d3d", 
            fg="#ffffff",
            bd=0,
            padx=15,
            pady=8,
            command=self.complete_base_tasks
        )
        complete_tasks_btn.pack(pady=20)
        
        # 添加说明文本
        desc = tk.Label(
            self.content_area, 
            text="点击后将自动完成基建中的所有可完成事项\n请确保已在首页界面，且游戏窗口可见", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc",
            justify=tk.CENTER
        )
        desc.pack(pady=10)
        
        # 添加阈值调整
        threshold_frame = tk.Frame(self.content_area, bg="#1a1a1a")
        threshold_frame.pack(pady=10)
        
        threshold_label = tk.Label(
            threshold_frame, 
            text="模板匹配阈值: ", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        threshold_label.pack(side=tk.LEFT, padx=5)
        
        self.threshold_var = tk.DoubleVar(value=0.8)
        threshold_scale = ttk.Scale(
            threshold_frame, 
            from_=0.1, 
            to=1.0, 
            orient="horizontal", 
            variable=self.threshold_var, 
            length=200
        )
        threshold_scale.pack(side=tk.LEFT)
        
        self.threshold_value_label = tk.Label(
            threshold_frame, 
            text=f"{self.threshold_var.get():.1f}", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        self.threshold_value_label.pack(side=tk.LEFT, padx=5)
        
        # 更新阈值显示
        def update_threshold_label(event):
            self.threshold_value_label.config(text=f"{self.threshold_var.get():.1f}")
        
        threshold_scale.bind("<Motion>", update_threshold_label)
        threshold_scale.bind("<ButtonRelease-1>", update_threshold_label)
        
    def show_combat(self):
        self.clear_content_area()
        title = tk.Label(
            self.content_area, 
            text="作战管理", 
            font=font.Font(family="SimHei", size=16, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        title.pack(pady=20)
        
        # 创建自动剿灭作战区域
        eliminate_frame = tk.Frame(self.content_area, bg="#1a1a1a")
        eliminate_frame.pack(pady=20, fill=tk.X)
        
        eliminate_title = tk.Label(
            eliminate_frame, 
            text="自动剿灭作战", 
            font=font.Font(family="SimHei", size=14, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        eliminate_title.pack(pady=10)
        
        # 轮次选择
        cycles_frame = tk.Frame(eliminate_frame, bg="#1a1a1a")
        cycles_frame.pack(pady=10)
        
        cycles_label = tk.Label(
            cycles_frame, 
            text="指定轮次: ", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        cycles_label.pack(side=tk.LEFT, padx=5)
        
        self.cycles_var = tk.IntVar(value=1)
        cycles_entry = tk.Entry(
            cycles_frame, 
            textvariable=self.cycles_var, 
            width=5, 
            font=font.Font(family="SimHei", size=10),
            bg="#2d2d2d", 
            fg="#ffffff",
            bd=0
        )
        cycles_entry.pack(side=tk.LEFT, padx=5)
        
        # 关卡选择下拉菜单
        level_frame = tk.Frame(cycles_frame, bg="#1a1a1a")
        level_frame.pack(side=tk.LEFT, padx=10)

        level_label = tk.Label(
            level_frame, 
            text="选择关卡: ", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        level_label.pack(side=tk.LEFT)

        self.level_var = tk.StringVar(value="龙门外环")
        level_option = ttk.Combobox(
            level_frame, 
            textvariable=self.level_var, 
            font=font.Font(family="SimHei", size=10),
            state="readonly",
            width=10
        )
        level_option['values'] = ("龙门外环", "龙门市区", "当期委托地点")
        level_option.pack(side=tk.LEFT)


        
        # 启动按钮
        start_eliminate_btn = tk.Button(
            eliminate_frame, 
            text="开始自动剿灭作战", 
            font=font.Font(family="SimHei", size=12),
            bg="#3d3d3d", 
            fg="#ffffff",
            bd=0,
            padx=15,
            pady=8,
            command=self.start_auto_eliminate
        )
        start_eliminate_btn.pack(pady=20)
        
        # 添加说明文本
        desc = tk.Label(
            eliminate_frame, 
            text="点击后将自动进行剿灭作战\n请确保已在主菜单界面\n请确保已解锁当前关卡的“代理指挥”功能", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc",
            justify=tk.CENTER
        )
        desc.pack(pady=10)
        
        # 添加阈值调整
        threshold_frame = tk.Frame(eliminate_frame, bg="#1a1a1a")
        threshold_frame.pack(pady=10)
        
        threshold_label = tk.Label(
            threshold_frame, 
            text="模板匹配阈值: ", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        threshold_label.pack(side=tk.LEFT, padx=5)
        
        self.combat_threshold_var = tk.DoubleVar(value=0.8)
        threshold_scale = ttk.Scale(
            threshold_frame, 
            from_=0.1, 
            to=1.0, 
            orient="horizontal", 
            variable=self.combat_threshold_var, 
            length=200
        )
        threshold_scale.pack(side=tk.LEFT)
        
        self.combat_threshold_value_label = tk.Label(
            threshold_frame, 
            text=f"{self.combat_threshold_var.get():.1f}", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        self.combat_threshold_value_label.pack(side=tk.LEFT, padx=5)
        
        # 更新阈值显示
        def update_combat_threshold_label(event):
            self.combat_threshold_value_label.config(text=f"{self.combat_threshold_var.get():.1f}")
        
        threshold_scale.bind("<Motion>", update_combat_threshold_label)
        threshold_scale.bind("<ButtonRelease-1>", update_combat_threshold_label)
        
    def show_recruit(self):
        self.clear_content_area()
        title = tk.Label(
            self.content_area, 
            text="招募管理", 
            font=font.Font(family="SimHei", size=16, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        title.pack(pady=20)
        
        # 招募标签选择区域
        tag_frame = tk.Frame(self.content_area, bg="#1a1a1a")
        tag_frame.pack(pady=10, fill=tk.X, padx=20)
        
        tag_title = tk.Label(
            tag_frame, 
            text="选择公开招募标签 (可多选)", 
            font=font.Font(family="SimHei", size=12, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        tag_title.pack(pady=10, anchor="w")
        
        # 标签列表
        tags = [
            "近卫干员", "近战位", "控场", "狙击干员", "重装干员", 
            "远程位", "爆发", "治疗", "医疗干员", "支援", 
            "辅助干员", "术师干员", "特种干员", "先锋干员", 
            "费用回复", "输出", "生存", "群攻", "防护", 
            "减速", "削弱", "快速复活", "位移", "召唤", 
            "支援机械", "元素", "新手"
        ]
        
        # 创建标签复选框
        self.tag_vars = {}
        tag_columns = 4
        tag_index = 0
        
        tag_check_frame = tk.Frame(tag_frame, bg="#1a1a1a")
        tag_check_frame.pack(fill=tk.X)
        
        for tag in tags:
            row = tag_index // tag_columns
            col = tag_index % tag_columns
            
            var = tk.BooleanVar(value=False)
            self.tag_vars[tag] = var
            
            check_btn = tk.Checkbutton(
                tag_check_frame, 
                text=tag, 
                variable=var, 
                font=font.Font(family="SimHei", size=10),
                bg="#1a1a1a", 
                fg="#cccccc",
                selectcolor="#3d3d3d",
                bd=0
            )
            check_btn.grid(row=row, column=col, sticky="w", padx=5, pady=5)
            
            tag_index += 1
        
        # 招募位选择
        slot_frame = tk.Frame(self.content_area, bg="#1a1a1a")
        slot_frame.pack(pady=10, fill=tk.X, padx=20)
        
        slot_label = tk.Label(
            slot_frame, 
            text="选择招募位", 
            font=font.Font(family="SimHei", size=12, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        slot_label.pack(side=tk.LEFT, padx=5)
        
        self.slot_var = tk.StringVar(value="所有")
        slot_option = ttk.Combobox(
            slot_frame, 
            textvariable=self.slot_var, 
            font=font.Font(family="SimHei", size=10),
            state="readonly",
            width=10
        )
        slot_option['values'] = ("所有", "1", "2", "3", "4")
        slot_option.pack(side=tk.LEFT, padx=5)
        
        # 阈值调整
        threshold_frame = tk.Frame(self.content_area, bg="#1a1a1a")
        threshold_frame.pack(pady=10, fill=tk.X, padx=20)
        
        threshold_label = tk.Label(
            threshold_frame, 
            text="模板匹配阈值: ", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        threshold_label.pack(side=tk.LEFT, padx=5)
        
        self.recruit_threshold_var = tk.DoubleVar(value=0.8)
        threshold_scale = ttk.Scale(
            threshold_frame, 
            from_=0.1, 
            to=1.0, 
            orient="horizontal", 
            variable=self.recruit_threshold_var, 
            length=200
        )
        threshold_scale.pack(side=tk.LEFT)
        
        self.recruit_threshold_value_label = tk.Label(
            threshold_frame, 
            text=f"{self.recruit_threshold_var.get():.1f}", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        self.recruit_threshold_value_label.pack(side=tk.LEFT, padx=5)
        
        # 更新阈值显示
        def update_recruit_threshold_label(event):
            self.recruit_threshold_value_label.config(text=f"{self.recruit_threshold_var.get():.1f}")
        
        threshold_scale.bind("<Motion>", update_recruit_threshold_label)
        threshold_scale.bind("<ButtonRelease-1>", update_recruit_threshold_label)
        
        # 开始招募按钮
        start_recruit_btn = tk.Button(
            self.content_area, 
            text="开始公开招募", 
            font=font.Font(family="SimHei", size=12),
            bg="#3d3d3d", 
            fg="#ffffff",
            bd=0,
            padx=15,
            pady=8,
            command=self.start_public_recruit
        )
        start_recruit_btn.pack(pady=20)
        
        # 添加说明文本
        desc = tk.Label(
            self.content_area, 
            text="点击后将自动进行公开招募\n请确保已在主菜单界面，且游戏窗口可见", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc",
            justify=tk.CENTER
        )
        desc.pack(pady=10)
        
    def show_settings(self):
        self.clear_content_area()
        title = tk.Label(
            self.content_area, 
            text="配置", 
            font=font.Font(family="SimHei", size=16, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        title.pack(pady=20)
        
        # 日志窗口设置区域
        log_settings_frame = tk.Frame(self.content_area, bg="#1a1a1a")
        log_settings_frame.pack(pady=20, fill=tk.X)
        
        log_settings_title = tk.Label(
            log_settings_frame, 
            text="日志窗口设置", 
            font=font.Font(family="SimHei", size=14, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        log_settings_title.pack(pady=10)

        # 截图存储设置
        screenshot_frame = tk.Frame(self.content_area, bg="#1a1a1a")
        screenshot_frame.pack(pady=20, fill=tk.X)

        screenshot_title = tk.Label(
            screenshot_frame, 
            text="截图存储设置", 
            font=font.Font(family="SimHei", size=14, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        screenshot_title.pack(pady=10)

        # 启用截图存储复选框
        self.save_screenshots_var = tk.BooleanVar(value=settings.SAVE_SCREENSHOTS)
        screenshot_check = tk.Checkbutton(
            screenshot_frame, 
            text="启用截图存储 (用于调试)", 
            variable=self.save_screenshots_var, 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc",
            selectcolor="#3d3d3d",
            bd=0,
            command=self.on_screenshot_toggle
        )
        screenshot_check.pack(pady=10, anchor="w")

        # 日志窗口设置区域

        
        # 启用日志窗口复选框
        self.log_window_enabled_var = tk.BooleanVar(value=settings.LOG_WINDOW_ENABLED)
        log_window_check = tk.Checkbutton(
            log_settings_frame, 
            text="启用日志窗口", 
            variable=self.log_window_enabled_var, 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc",
            selectcolor="#3d3d3d",
            bd=0, 
            command=self.toggle_log_window
        )
        log_window_check.pack(pady=10, anchor="w")
        
        # 日志窗口透明度调整
        opacity_frame = tk.Frame(log_settings_frame, bg="#1a1a1a")
        opacity_frame.pack(pady=10, fill=tk.X)
        
        opacity_label = tk.Label(
            opacity_frame, 
            text="日志窗口不透明度: ", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        opacity_label.pack(side=tk.LEFT, padx=5)
        
        self.opacity_var = tk.DoubleVar(value=settings.LOG_WINDOW_OPACITY)
        opacity_scale = ttk.Scale(
            opacity_frame, 
            from_=0.1, 
            to=1.0, 
            orient="horizontal", 
            variable=self.opacity_var, 
            length=200, 
            command=self.update_log_window_opacity
        )
        opacity_scale.pack(side=tk.LEFT)
        
        self.opacity_value_label = tk.Label(
            opacity_frame, 
            text=f"{self.opacity_var.get():.1f}", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        self.opacity_value_label.pack(side=tk.LEFT, padx=5)

        # 日志窗口宽度调整
        width_frame = tk.Frame(log_settings_frame, bg="#1a1a1a")
        width_frame.pack(pady=10, fill=tk.X)

        width_label = tk.Label(
            width_frame, 
            text="日志窗口宽度: ", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        width_label.pack(side=tk.LEFT, padx=5)

        self.width_var = tk.IntVar(value=settings.LOG_WINDOW_WIDTH)
        width_scale = ttk.Scale(
            width_frame, 
            from_=400, 
            to=1600, 
            orient="horizontal", 
            variable=self.width_var, 
            length=200, 
            command=self.update_log_window_width
        )
        width_scale.pack(side=tk.LEFT)

        self.width_value_label = tk.Label(
            width_frame, 
            text=f"{self.width_var.get()}", 
            font=font.Font(family="SimHei", size=10),
            bg="#1a1a1a", 
            fg="#cccccc"
        )
        self.width_value_label.pack(side=tk.LEFT, padx=5)

        # 更新宽度显示
        def update_width_label(event):
            self.width_value_label.config(text=f"{self.width_var.get()}")

        width_scale.bind("<Motion>", update_width_label)
        width_scale.bind("<ButtonRelease-1>", update_width_label)
        
        # 更新透明度显示
        def update_opacity_label(event):
            self.opacity_value_label.config(text=f"{self.opacity_var.get():.1f}")
        
        opacity_scale.bind("<Motion>", update_opacity_label)
        opacity_scale.bind("<ButtonRelease-1>", update_opacity_label)
        
        # 保存配置按钮
        save_btn = tk.Button(
            log_settings_frame, 
            text="保存配置", 
            font=font.Font(family="SimHei", size=12),
            bg="#3d3d3d", 
            fg="#ffffff",
            bd=0, 
            padx=15, 
            pady=8, 
            command=self.save_settings
        )
        save_btn.pack(pady=20)
        
    def init_log_window(self):
        """
        初始化日志窗口
        """
        # 创建日志窗口
        self.log_window = tk.Toplevel(self.root)
        self.log_window.title("ZOOT 日志")
        
        # 隐藏窗口边框
        self.log_window.overrideredirect(True)
        
        # 设置窗口位置在屏幕左下角
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 使用配置文件中的窗口宽度
        window_width = settings.LOG_WINDOW_WIDTH
        window_height = settings.LOG_WINDOW_HEIGHT
        self.log_window.geometry(f"{window_width}x{window_height}+0+{screen_height-window_height}")
        
        # 设置窗口透明度
        self.log_window.attributes('-alpha', settings.LOG_WINDOW_OPACITY)
        
        # 确保窗口置顶
        self.log_window.attributes('-topmost', True)
        
        # 创建滚动文本框用于显示日志
        self.log_text = scrolledtext.ScrolledText(
            self.log_window, 
            wrap=tk.WORD, 
            bg="#1a1a1a", 
            fg="#cccccc", 
            font=font.Font(family="SimHei", size=10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 创建自定义日志处理器
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                logging.Handler.__init__(self)
                self.text_widget = text_widget
                self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

            def emit(self, record):
                msg = self.format(record) + '\n'
                self.text_widget.configure(state='normal')
                self.text_widget.insert(tk.END, msg)
                self.text_widget.see(tk.END)  # 滚动到最后一行
                self.text_widget.configure(state='disabled')

        # 添加日志处理器到logger
        self.text_handler = TextHandler(self.log_text)
        logger.addHandler(self.text_handler)
        
        # 根据配置决定是否显示日志窗口
        if not settings.LOG_WINDOW_ENABLED:
            self.log_window.withdraw()

    def show_about(self):
        self.clear_content_area()
        title = tk.Label(
            self.content_area, 
            text="关于", 
            font=font.Font(family="SimHei", size=16, weight="bold"),
            bg="#1a1a1a", 
            fg="#ffffff"
        )
        title.pack(pady=20)
        
        about_text = "ZOOT Acting Commander\n\n版本: 0.1.0\n\n基于Python开发的明日方舟自动化工具\nbeta阶段\n\n开发者: @bilibili_没事干的雀斑猪\n\n联系: 3919086204@qq.com"

        about_label = tk.Label(
            self.content_area, 
            text=about_text, 
            font=font.Font(family="SimHei", size=12),
            bg="#1a1a1a", 
            fg="#cccccc",
            justify=tk.CENTER
        )
        about_label.pack()
        
    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def on_move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y
        self.root.geometry(f"+{x}+{y}")

        
    def complete_base_tasks(self):
        """
        完成基建事项功能
        """
        try:
            threshold = self.threshold_var.get()
            logger.info("开始执行完成基建事项功能...")
            logger.info(f"当前模板匹配阈值: {threshold}")
            
            # 显示提示信息
            messagebox.showinfo("提示", "请确保已在主菜单界面\n3秒后开始执行...")
            
            # 等待3秒
            time.sleep(3)
            
            # 隐藏窗口
            self.root.withdraw()
            
            # 使用已初始化的基建管理模块实例
            logger.info("正在导航到基建...")
            if not self.base_manager.navigate_to_base(threshold=threshold):
                logger.error("无法导航到基建")
                messagebox.showerror("失败", "无法导航到基建")
                return
            time.sleep(10)
            
            logger.info("正在尝试完成事项...")
            # 完成事项
            success = self.base_manager.complete_tasks(threshold=threshold)
            
            if success:
                logger.info("完成事项成功!")
                messagebox.showinfo("成功", "基建事项已成功完成!")
            else:
                logger.error("完成事项失败!")
                messagebox.showerror("失败", "无法完成基建事项，请检查游戏界面是否正确。")
        except ElementNotFoundError as e:
            logger.error(f"执行失败: 未找到元素 - {e}")
            messagebox.showerror("失败", f"未找到元素: {e}\n可能的原因: 游戏窗口未正确唤出、界面与模板不匹配或通知按钮不可见")
        except OperationFailedError as e:
            logger.error(f"执行失败: 操作失败 - {e}")
            messagebox.showerror("失败", f"操作失败: {e}\n可能的原因: 鼠标点击操作未能正确执行")
        except Exception as e:
            logger.error(f"执行过程中发生未知错误: {str(e)}")
            messagebox.showerror("错误", f"发生未知错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # 显示窗口
            self.root.deiconify()
        
    def start_auto_eliminate(self):
        """
        自动剿灭作战功能
        """
        try:
            cycles = self.cycles_var.get()
            threshold = self.combat_threshold_var.get()
            
            if cycles <= 0:
                messagebox.showerror("错误", "轮次必须大于0")
                return
            
            logger.info("开始执行自动剿灭作战功能...")
            logger.info(f"轮次: {cycles}, 模板匹配阈值: {threshold}")
            
            # 显示提示信息
            messagebox.showinfo("提示", "请确保已在主菜单界面\n3秒后开始执行...")
            
            # 等待3秒
            time.sleep(3)
            
            # 隐藏窗口
            self.root.withdraw()
            
            # 使用已初始化的作战模块实例
            logger.info("正在导航到作战界面...")
            if not self.combat_manager.navigate_to_mission(threshold=threshold):
                logger.error("无法导航到作战界面")
                messagebox.showerror("失败", "无法导航到作战界面")
                return
            time.sleep(2)
            
            # 导航到常态事务
            logger.info("正在导航到常态事务...")
            if not self.combat_manager.navigate_to_normal_affairs(threshold=threshold):
                logger.error("无法导航到常态事务")
                messagebox.showerror("失败", "无法导航到常态事务")
                return
            time.sleep(2)
            
            # 导航到剿灭作战
            logger.info("正在导航到剿灭作战...")
            if not self.combat_manager.navigate_to_eliminate(threshold=threshold):
                logger.error("无法导航到剿灭作战")
                messagebox.showerror("失败", "无法导航到剿灭作战")
                return
            time.sleep(2)
            
            # 根据选择的关卡导航
            selected_level = self.level_var.get()
            logger.info(f"正在导航到{selected_level}...")
            
            if selected_level == "龙门外环":
                if not self.combat_manager.navigate_to_longmen(threshold=threshold):
                    logger.error(f"无法导航到{selected_level}")
                    messagebox.showerror("失败", f"无法导航到{selected_level}")
                    return
            elif selected_level == "龙门市区":
                if not self.combat_manager.navigate_to_longmen_city(threshold=threshold):
                    logger.error(f"无法导航到{selected_level}")
                    messagebox.showerror("失败", f"无法导航到{selected_level}")
                    return
            elif selected_level == "当期委托地点":
                if not self.combat_manager.navigate_to_current_commission(threshold=threshold):
                    logger.error(f"无法导航到{selected_level}")
                    messagebox.showerror("失败", f"无法导航到{selected_level}")
                    return
            # 未来可以在这里添加其他关卡的导航逻辑
            # elif selected_level == "其他关卡名称":
            #     if not combat_manager.navigate_to_other_level(threshold=threshold):
            #         logger.error(f"无法导航到{selected_level}")
            #         messagebox.showerror("失败", f"无法导航到{selected_level}")
            #         return
            
            time.sleep(2)
            
            # 检查并启用代理指挥
            logger.info("正在检查并启用代理指挥...")
            acting_commander_success = self.combat_manager.check_and_enable_acting_commander(threshold=threshold)
            if not acting_commander_success:
                logger.error("无法启用代理指挥")
                messagebox.showerror("失败", "无法启用代理指挥")
                return
            time.sleep(2)
            
            # 开始作战循环
            logger.info(f"开始作战循环，轮次: {cycles}")
            
            # 执行作战循环
            success = self.combat_manager.combat_only_flow(cycles=cycles, threshold=threshold)
            
            if success:
                logger.info(f"自动剿灭作战完成，共执行 {cycles} 轮")
                messagebox.showinfo("成功", f"自动剿灭作战完成，共执行 {cycles} 轮")
            else:
                logger.error("自动剿灭作战失败")
                messagebox.showerror("失败", "自动剿灭作战失败，请检查游戏界面是否正确。")
        except ElementNotFoundError as e:
            logger.error(f"执行失败: 未找到元素 - {e}")
            messagebox.showerror("失败", f"未找到元素: {e}\n可能的原因: 游戏窗口未正确唤出、界面与模板不匹配")
        except OperationFailedError as e:
            logger.error(f"执行失败: 操作失败 - {e}")
            messagebox.showerror("失败", f"操作失败: {e}\n可能的原因: 鼠标点击操作未能正确执行")
        except Exception as e:
            logger.error(f"执行过程中发生未知错误: {str(e)}")
            messagebox.showerror("错误", f"发生未知错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # 显示窗口
            self.root.deiconify()
        
    def start_public_recruit(self):
        """
        公开招募功能
        """
        try:
            # 导入招募模块
            from modules import RecruitModule
            
            # 获取选中的标签
            selected_tags = [tag for tag, var in self.tag_vars.items() if var.get()]
            
            # 获取选择的招募位
            slot_option = self.slot_var.get()
            slot_number = None if slot_option == "所有" else int(slot_option)
            
            # 获取模板匹配阈值
            threshold = self.recruit_threshold_var.get()
            
            logger.info(f"开始执行公开招募功能...")
            logger.info(f"选中的标签: {selected_tags}")
            logger.info(f"选择的招募位: {slot_option}")
            logger.info(f"模板匹配阈值: {threshold}")
            
            # 如果没有选择标签，使用默认标签
            if not selected_tags:
                selected_tags = ["重装干员", "新手", "医疗干员"]
                logger.info(f"未选择标签，使用默认标签: {selected_tags}")
            
            # 显示提示信息
            messagebox.showinfo("提示", "请确保已在主菜单界面\n3秒后开始执行...")
            
            # 等待3秒
            time.sleep(3)
            
            # 隐藏窗口
            self.root.withdraw()
            
            # 创建招募模块实例
            recruit_manager = RecruitModule()
            
            # 导航到招募页面
            logger.info("正在导航到招募页面...")
            if not recruit_manager.navigate_to_recruit(threshold=threshold):
                logger.error("无法导航到招募页面")
                messagebox.showerror("失败", "无法导航到招募页面")
                return
            time.sleep(2)
            
            # 执行招募操作
            logger.info(f"正在执行招募操作，目标标签: {selected_tags}")
            success = recruit_manager.enter_recruit_slots(slot_number=slot_number, target_tags=selected_tags, threshold=threshold)
            
            if success:
                logger.info("公开招募操作完成!")
                messagebox.showinfo("成功", "公开招募操作已完成!")
            else:
                logger.error("公开招募操作失败!")
                messagebox.showerror("失败", "无法完成公开招募操作，请检查游戏界面是否正确。")
        except ElementNotFoundError as e:
            logger.error(f"执行失败: 未找到元素 - {e}")
            messagebox.showerror("失败", f"未找到元素: {e}\n可能的原因: 游戏窗口未正确唤出、界面与模板不匹配")
        except OperationFailedError as e:
            logger.error(f"执行失败: 操作失败 - {e}")
            messagebox.showerror("失败", f"操作失败: {e}\n可能的原因: 鼠标点击操作未能正确执行")
        except Exception as e:
            logger.error(f"执行过程中发生未知错误: {str(e)}")
            messagebox.showerror("错误", f"发生未知错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # 显示窗口
            self.root.deiconify()

    def claim_task_rewards(self):
        """
        领取任务奖励功能
        """
        try:
            logger.info("开始执行领取任务奖励功能...")
            
            # 显示提示信息
            messagebox.showinfo("提示", "请确保已在主菜单界面\n3秒后开始执行...")
            
            # 等待3秒
            time.sleep(3)
            
            # 隐藏窗口
            self.root.withdraw()
            
            logger.info("正在尝试领取任务奖励...")
            # 使用已初始化的任务管理模块实例领取奖励
            success = self.task_manager.claim_all_rewards()
            
            if success:
                logger.info("领取任务奖励成功!")
                messagebox.showinfo("成功", "任务奖励已成功领取!")
            else:
                logger.error("领取任务奖励失败!")
                messagebox.showerror("失败", "无法领取任务奖励，请检查游戏界面是否正确。")
        except ElementNotFoundError as e:
            logger.error(f"执行失败: 未找到元素 - {e}")
            messagebox.showerror("失败", f"未找到元素: {e}\n可能的原因: 游戏窗口未正确唤出、界面与模板不匹配")
        except OperationFailedError as e:
            logger.error(f"执行失败: 操作失败 - {e}")
            messagebox.showerror("失败", f"操作失败: {e}\n可能的原因: 鼠标点击操作未能正确执行")
        except Exception as e:
            logger.error(f"执行过程中发生未知错误: {str(e)}")
            messagebox.showerror("错误", f"发生未知错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # 显示窗口
            self.root.deiconify()
        
    def toggle_log_window(self):
        """
        切换日志窗口的显示/隐藏状态
        """
        if self.log_window_enabled_var.get():
            self.log_window.deiconify()
        else:
            self.log_window.withdraw()

    def on_screenshot_toggle(self):
        """
        处理截图存储复选框的切换事件
        """
        save_state = self.save_screenshots_var.get()
        logger.info(f"截图存储状态已切换为: {'启用' if save_state else '禁用'}")
        # 立即保存设置
        self.save_settings()

    def update_log_window_opacity(self, value):
        """
        更新日志窗口的透明度
        """
        try:
            opacity = float(value)
            self.opacity_value_label.config(text=f"{opacity:.1f}")
            if hasattr(self, 'log_window') and self.log_window_enabled_var.get():
                self.log_window.attributes('-alpha', opacity)
        except ValueError:
            pass

    def update_log_window_width(self, value):
        """
        更新日志窗口的宽度
        """
        try:
            width = int(float(value))
            self.width_value_label.config(text=f"{width}")
            if hasattr(self, 'log_window') and self.log_window_enabled_var.get():
                screen_height = self.root.winfo_screenheight()
                window_height = self.log_window.winfo_height()
                self.log_window.geometry(f"{width}x{window_height}+0+{screen_height-window_height}")
        except ValueError:
            pass

    def save_settings(self):
        """
        保存配置到文件
        """
        try:
            # 更新设置
            settings.LOG_WINDOW_ENABLED = self.log_window_enabled_var.get()
            settings.LOG_WINDOW_OPACITY = self.opacity_var.get()
            settings.LOG_WINDOW_WIDTH = self.width_var.get()
            settings.SAVE_SCREENSHOTS = self.save_screenshots_var.get()
            
            # 保存到文件
            config_file_path = os.path.join(project_root, 'config', 'settings.py')
            with open(config_file_path, 'w', encoding='utf-8') as f:
                f.write('# 配置文件\n\n')
                f.write('class Settings:\n')
                f.write('    # 日志窗口设置\n')
                f.write(f'    LOG_WINDOW_ENABLED = {settings.LOG_WINDOW_ENABLED}\n')
                f.write(f'    LOG_WINDOW_OPACITY = {settings.LOG_WINDOW_OPACITY:.1f}\n')
                f.write(f'    LOG_WINDOW_WIDTH = {settings.LOG_WINDOW_WIDTH}     # 日志窗口宽度\n')
                f.write('    LOG_WINDOW_HEIGHT = 300    # 日志窗口高度\n')
                f.write('    \n')
                f.write('    # 截图存储设置\n')
                f.write(f'    SAVE_SCREENSHOTS = {settings.SAVE_SCREENSHOTS}    # 是否保存截图用于调试\n\n')
                f.write('# 创建设置实例\n')
                f.write('settings = Settings()\n')
            
            logger.info("配置已保存成功")
            messagebox.showinfo("成功", "配置已保存成功")
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
            messagebox.showerror("失败", f"保存配置失败: {str(e)}")

    def on_closing(self):
        # 退出程序
        self.root.destroy()
        
def main():
    import tkinter as tk
    root = tk.Tk()
    app = ZOOTGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()