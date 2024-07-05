// based on https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/v1.6.0/javascript/contextMenus.js

//const FLASK_API = 'http://0.0.0.0:5001';
const FLASK_API = 'https://z6oyjsb9pla5ng-5001.proxy.runpod.net';

var contextMenuInit = function () {
  let eventListenerApplied = false;
  let menuSpecs = new Map();

  const uid = function () {
    return Date.now().toString(36) + Math.random().toString(36).substring(2);
  };

  function showContextMenu(event, element, menuEntries) {
    let posx =
      event.clientX +
      document.body.scrollLeft +
      document.documentElement.scrollLeft;
    let posy =
      event.clientY +
      document.body.scrollTop +
      document.documentElement.scrollTop;

    let oldMenu = gradioApp().querySelector('#context-menu');
    if (oldMenu) {
      oldMenu.remove();
    }

    let baseStyle = window.getComputedStyle(
      gradioApp().querySelector('button.selected')
    );

    const contextMenu = document.createElement('nav');
    contextMenu.id = 'context-menu';
    contextMenu.style.background = baseStyle.background;
    contextMenu.style.color = baseStyle.color;
    contextMenu.style.fontFamily = baseStyle.fontFamily;
    contextMenu.style.top = posy + 'px';
    contextMenu.style.left = posx + 'px';

    const contextMenuList = document.createElement('ul');
    contextMenuList.className = 'context-menu-items';
    contextMenu.append(contextMenuList);

    menuEntries.forEach(function (entry) {
      let contextMenuEntry = document.createElement('a');
      contextMenuEntry.innerHTML = entry['name'];
      contextMenuEntry.addEventListener('click', function () {
        entry['func']();
      });
      contextMenuList.append(contextMenuEntry);
    });

    gradioApp().appendChild(contextMenu);

    let menuWidth = contextMenu.offsetWidth + 4;
    let menuHeight = contextMenu.offsetHeight + 4;

    let windowWidth = window.innerWidth;
    let windowHeight = window.innerHeight;

    if (windowWidth - posx < menuWidth) {
      contextMenu.style.left = windowWidth - menuWidth + 'px';
    }

    if (windowHeight - posy < menuHeight) {
      contextMenu.style.top = windowHeight - menuHeight + 'px';
    }
  }

  function appendContextMenuOption(
    targetElementSelector,
    entryName,
    entryFunction
  ) {
    var currentItems = menuSpecs.get(targetElementSelector);

    if (!currentItems) {
      currentItems = [];
      menuSpecs.set(targetElementSelector, currentItems);
    }
    let newItem = {
      id: targetElementSelector + '_' + uid(),
      name: entryName,
      func: entryFunction,
      isNew: true,
    };

    currentItems.push(newItem);
    return newItem['id'];
  }

  function removeContextMenuOption(uid) {
    menuSpecs.forEach(function (v) {
      let index = -1;
      v.forEach(function (e, ei) {
        if (e['id'] == uid) {
          index = ei;
        }
      });
      if (index >= 0) {
        v.splice(index, 1);
      }
    });
  }

  function addContextMenuEventListener() {
    if (eventListenerApplied) {
      return;
    }
    gradioApp().addEventListener('click', function (e) {
      if (!e.isTrusted) {
        return;
      }

      let oldMenu = gradioApp().querySelector('#context-menu');
      if (oldMenu) {
        oldMenu.remove();
      }
    });
    gradioApp().addEventListener('contextmenu', function (e) {
      let oldMenu = gradioApp().querySelector('#context-menu');
      if (oldMenu) {
        oldMenu.remove();
      }
      menuSpecs.forEach(function (v, k) {
        if (e.composedPath()[0].matches(k)) {
          showContextMenu(e, e.composedPath()[0], v);
          e.preventDefault();
        }
      });
    });
    eventListenerApplied = true;
  }

  return [
    appendContextMenuOption,
    removeContextMenuOption,
    addContextMenuEventListener,
  ];
};

function handleModal() {
  const modal = document.createElement('div');
  modal.setAttribute('id', 'myModal');
  modal.classList.add('modal');

  // Crear el contenido del modal
  const modalContent = document.createElement('div');
  modalContent.classList.add('modal-content');

  // Crear el botón para cerrar el modal
  var closeBtn = document.createElement('span');
  closeBtn.classList.add('close');
  closeBtn.innerHTML = '&times;';
  closeBtn.onclick = function () {
    modal.style.display = 'none';
  };
  modalContent.appendChild(closeBtn);
  const form_container = document.createElement('div');

  const question_one = 'What did you think of the Mystica IA?';
  const question_two = 'What features would you like to have in Mystica IA?';
  const question_three = 'What did you like most about Mystica IA?';
  const list_Questions = [question_one, question_two, question_three];
  // Crear los inputs
  for (let i = 1; i <= 3; i++) {
    var label = document.createElement('label');
    var input = document.createElement('input');
    var div = document.createElement('div');

    label.textContent = list_Questions[i - 1];
    input.setAttribute('type', 'text');
    input.setAttribute('id', 'input' + i);
    input.setAttribute('placeholder', 'Type your answer here...');
    div.appendChild(label);
    div.appendChild(input);
    div.classList.add('group');
    label.classList.add('label_form');
    form_container.appendChild(div);
    form_container.classList.add('container_form');
  }
  modalContent.appendChild(form_container);
  // Crear el botón para enviar
  var submitBtn = document.createElement('button');
  submitBtn.textContent = 'Enviar';
  submitBtn.classList.add('btn_form');
  submitBtn.onclick = function () {
    // Aquí puedes realizar acciones con los valores de los inputs
    var answer_one = document.getElementById('input1').value;
    var answer_two = document.getElementById('input2').value;
    var answer_three = document.getElementById('input3').value;
    var username = document.getElementById('username').textContent;

    const datos = {
      answer_one,
      answer_two,
      answer_three,
      username,
    };
    var jsonData = JSON.stringify(datos);
    const url = FLASK_API + '/feedbacks';

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonData,
    });

    modal.style.display = 'none'; // Ocultar el modal después de hacer clic en enviar
  };
  modalContent.appendChild(submitBtn);

  modal.appendChild(modalContent);

  document.body.appendChild(modal);

  const openModalBtn = document.getElementById('open_modal');

  console.log(openModalBtn);
  // Cuando el usuario haga clic en el botón, abrir el modal
  openModalBtn.onclick = function () {
    modal.style.display = 'block';
  };

  // Cuando el usuario haga clic en el botón de cierre, cerrar el modal
  document.addEventListener('click', function (event) {
    if (event.target.classList.contains('close')) {
      event.target.closest('.modal').style.display = 'none';
    }
  });
}

var initResponse = contextMenuInit();
console.log({ initResponse });

var appendContextMenuOption = initResponse[0];
var removeContextMenuOption = initResponse[1];
var addContextMenuEventListener = initResponse[2];

let cancelGenerateForever = function () {
  clearInterval(window.generateOnRepeatInterval);
};

(function () {
  //Start example Context Menu Items
  let generateOnRepeat = function (genbuttonid, interruptbuttonid) {
    let genbutton = gradioApp().querySelector(genbuttonid);
    let interruptbutton = gradioApp().querySelector(interruptbuttonid);
    if (!interruptbutton.offsetParent) {
      genbutton.click();
    }
    clearInterval(window.generateOnRepeatInterval);
    window.generateOnRepeatInterval = setInterval(function () {
      if (!interruptbutton.offsetParent) {
        genbutton.click();
      }
    }, 500);
  };

  let generateOnRepeatForButtons = function () {
    generateOnRepeat('#generate_button', '#stop_button');
  };
  appendContextMenuOption(
    '#generate_button',
    'Generate forever',
    generateOnRepeatForButtons
  );
})();
//End example Context Menu Items

document.onreadystatechange = function () {
  if (document.readyState == 'complete') {
    addContextMenuEventListener();
  }
};
