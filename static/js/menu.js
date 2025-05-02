// 新版递归菜单渲染
function initMenu() {
  fetch('/static/menu.json')
    .then(res => res.json())
    .then(data => {
      const container = document.querySelector('.side-menu');
      container.appendChild(
        createMenuItems(data.menu_items)
      );
      container.addEventListener('click', function(e) {
        // 处理菜单点击
        const menuLink = e.target.closest('a[href]');
        if (menuLink) {
          e.preventDefault();
          const url = menuLink.getAttribute('href');
          
          // AJAX加载内容
          fetch(url)
            .then(response => response.text())
            .then(html => {
              document.getElementById('content-frame').innerHTML = html;
              history.pushState(null, '', url);
            });
        }
        
        // 处理子菜单展开
        const menuItem = e.target.closest('.has-children');
        if (menuItem) {
          menuItem.classList.toggle('expanded');
          e.stopPropagation();
          const subContainer = menuItem.querySelector('.submenu-container');
          subContainer.style.maxHeight = subContainer.style.maxHeight ? null : subContainer.scrollHeight + 'px';
        }
      });
    });
}

function createMenuItems(items, level = 0) {
  const ul = document.createElement('ul');
  ul.className = 'menu-list';
  
  items.forEach(item => {
    const li = document.createElement('li');
    li.className = 'menu-item' + (item.submenu ? ' has-children' : '');
    
    // 菜单链接
    const a = document.createElement('a');
    a.className = 'menu-link';
    a.href = item.url || '#';
    a.innerHTML = `
      <svg class="menu-icon" viewBox="0 0 24 24">
        <use xlink:href="#${item.icon}"></use>
      </svg>
      ${item.title}
    `;
    
    // 子菜单切换按钮
    if (item.submenu) {
      const toggle = document.createElement('span');
      toggle.className = 'submenu-toggle';
      toggle.innerHTML = '▶';
      a.appendChild(toggle);
    }
    
    li.appendChild(a);
    
    // 递归生成子菜单
    if (item.submenu) {
      const subContainer = document.createElement('div');
      subContainer.className = 'submenu-container';
      subContainer.appendChild(createMenuItems(item.submenu, level + 1));
      li.appendChild(subContainer);
    }
    
    ul.appendChild(li);
  });
  
  return ul;
}

// 处理菜单点击事件
document.addEventListener('DOMContentLoaded', initMenu);