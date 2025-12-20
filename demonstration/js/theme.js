// 主题切换功能
class ThemeManager {
  constructor() {
    this.currentTheme = 'light';
    this.init();
  }

  init() {
    // 从localStorage获取保存的主题，如果没有则默认为亮色主题
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      this.currentTheme = savedTheme;
    } else {
      // 检查系统偏好
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        this.currentTheme = 'dark';
      }
    }

    // 应用主题
    this.applyTheme();

    // 监听系统主题变化
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      mediaQuery.addListener((e) => {
        if (this.currentTheme === 'auto') {
          this.applyTheme();
        }
      });
    }
  }

  applyTheme() {
    let theme = this.currentTheme;

    // 如果设置为auto，根据系统偏好确定主题
    if (theme === 'auto') {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        theme = 'dark';
      } else {
        theme = 'light';
      }
    }

    // 应用到HTML元素
    document.documentElement.setAttribute('data-theme', theme);

    // 更新meta主题色（移动端状态栏）
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', theme === 'dark' ? '#111827' : '#ffffff');
    }
  }

  setTheme(theme) {
    this.currentTheme = theme;
    localStorage.setItem('theme', theme);
    this.applyTheme();

    // 触发自定义事件
    window.dispatchEvent(new CustomEvent('themeChange', {
      detail: { theme }
    }));
  }

  getTheme() {
    return this.currentTheme;
  }

  toggle() {
    const themes = ['light', 'dark', 'auto'];
    const currentIndex = themes.indexOf(this.currentTheme);
    const nextIndex = (currentIndex + 1) % themes.length;
    this.setTheme(themes[nextIndex]);
  }
}

// 创建全局主题管理器实例
const themeManager = new ThemeManager();

// 初始化主题切换按钮
function initThemeSwitcher() {
  const buttons = document.querySelectorAll('.theme-button');
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const theme = button.getAttribute('data-theme');
      if (theme) {
        themeManager.setTheme(theme);
        updateThemeButtons();
      }
    });
  });

  updateThemeButtons();
}

// 更新主题按钮状态
function updateThemeButtons() {
  const buttons = document.querySelectorAll('.theme-button');
  buttons.forEach(button => {
    const theme = button.getAttribute('data-theme');
    if (theme === themeManager.getTheme()) {
      button.classList.add('active');
    } else {
      button.classList.remove('active');
    }
  });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
  initThemeSwitcher();
});

// 导出主题管理器供其他脚本使用
window.themeManager = themeManager;
