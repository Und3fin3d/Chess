const sq = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

let drag;
let beingDragged;
let start;
let shiftX
let shiftY
let lastX
let lastY
let over
let overlay = document.createElement('div')
document.body.appendChild(overlay);
function init(pieces){
  let center = document.createElement('div');
  let ChessBoard = document.createElement('div');
  ChessBoard.setAttribute('class','chessboard')
  if (pieces){
    for (let i = 0; i <8; i++)  {
      let tr = document.createElement('div');
      tr.setAttribute('class','row')
      for (let j = 7; j >-1; j--) {
        let td = document.createElement('div');
          td.id = sq[j]+(i+1)
        if ((i + j) % 2 == 1) {
          td.setAttribute('class', 'square white');
          tr.appendChild(td);
        }
        else {
          td.setAttribute('class', 'square black');
          tr.appendChild(td);
        }
      }
      ChessBoard.appendChild(tr);
    }
  }
  else{
    for (let i = 7; i >-1; i--) {
      let tr = document.createElement('div');
      tr.setAttribute('class','row')
      for (let j = 0; j < 8; j++) {
        let td = document.createElement('div');
          td.id = sq[j]+(i+1)
        if ((i + j) % 2 == 1) {
          td.setAttribute('class', 'square white');
          tr.appendChild(td);
        }
        else {
          td.setAttribute('class', 'square black');
          tr.appendChild(td);
        }
      }
      ChessBoard.appendChild(tr);
    }
  }
  center.appendChild(ChessBoard);
  document.body.appendChild(center);
} 
let legalmoves = ['b1c3', 'b1a3', 'g1h3', 'g1f3', 'a2a4', 'a2a3', 'b2b4', 'b2b3', 'c2c4', 'c2c3', 'd2d4', 'd2d3', 'e2e4', 'e2e3', 'f2f4', 'f2f3', 'g2g4', 'g2g3', 'h2h4', 'h2h3']
function drawboard(board){
  for (let i = 0; i <8; i++){
    for (let j = 0; j<8; j++){
      let square = document.getElementById(sq[j]+(i+1))
      square.innerHTML = '';
      if (board[i][j] !=='•'){
        let img = document.createElement('img');
        img.setAttribute('id',board[i][j])
        img.src = "../static/images/" + board[i][j]+".svg";
        img.addEventListener('dragstart',function(e){
          beingDragged = e.target;
          start = e.target.parentNode.id
        });
        img.addEventListener('touchstart', function(e) {
          beingDragged = img;
          start = e.target.parentNode.id;
          img.style.zIndex = 1;
          shiftX = e.touches[0].clientX-(img.width/2);
          shiftY = e.touches[0].clientY - (img.height/2);
        });
        img.addEventListener("touchmove", function(e) {
          e.preventDefault();
          lastX =e.touches[0].clientX 
          lastY = e.touches[0].clientY
          img.style.left=lastX-shiftX+"px";
          img.style.top=lastY-shiftY+"px";
          let tar = document.elementsFromPoint(lastX,lastY)[1]
          if (tar != document.getElementById(start)){
            if(tar.tagName=="DIV" && !tar.hasChildNodes()){
              if(over!=null){
                over.classList.remove('highlight')
                over.classList.remove('highlight2')
              }
              over = tar
              over.classList.add('highlight')
            }
            else if(tar.tagName=="IMG" && isLowerCase(tar.id) != isLowerCase(img.id)){
              if(over!=null){
                over.classList.remove('highlight')
                over.classList.remove('highlight2')
              }
              over = tar.parentNode
              over.classList.add('highlight2')
            }
          }
        });
        img.addEventListener("touchend", function(e) {
          e.preventDefault()
          img.style.zIndex = "";
          let sq = document.elementsFromPoint(lastX,lastY)[1]
          if (sq.tagName=="IMG"){
            sq = sq.parentNode
          }
          let move = start + sq.id
          if (isLowerCase(img.id)==colour){
            if (img.id.toLowerCase()=='k'){
              if(start.substring(0,1)=='e'){
                if(sq.id.substring(0,1)=='c'){
                  move = 'O-O-O'
                }
                if(sq.id.substring(0,1)=='g'){
                  move = 'O-O'
                }
              }
            }
            if (legalmoves.includes(move)){
              if(sq.children.length != 0){
                if (isLowerCase(sq.children[0].id) != isLowerCase(img.id)){
                  sq.textContent = '';
                  sq.append(img)
                  img.style.left = "50%"
                  img.style.top = "50%"
                  POST(move)
                  over.classList.remove('highlight')
                  over.classList.remove('highlight2')
                }
              }
              else{
                sq.append(img)
                img.style.left = "50%"
                img.style.top = "50%"
                POST(move)
                over.classList.remove('highlight')
                over.classList.remove('highlight2')
              }
            }
            else if (legalmoves.includes(move+'P')){
              sq.innerHTML = ''
              over.classList.remove('highlight2')
              for (let i = 7; i >4; i--) {
                let s = document.getElementById(sq.id.substring(0,1)+i)
                s.innerHTML = ''
              }
              overlay.classList.add('overlay');
              fillProm(['Q','N','B','R'],move)
              sq.appendChild(promotion);
            }
            else{
                img.style.top = "50%"
                img.style.left = "50%"
                over.classList.remove('highlight')
                over.classList.remove('highlight2')
            }
          }
        });
        square.appendChild(img);
      }
    }
  }
}
function isLowerCase(str){
    return str == str.toLowerCase() && str != str.toUpperCase();
}
function removehigh(targets,clas){
  targets.forEach(target =>{
    target.classList.remove(clas);
  });
}
let colour = false
init(colour)
let board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
             ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
             ['•', '•', '•', '•', '•', '•', '•', '•'],
             ['•', '•', '•', '•', '•', '•', '•', '•'],
             ['•', '•', '•', '•', '•', '•', '•', '•'],
             ['•', '•', '•', '•', '•', '•', '•', '•'],
             ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
             ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']];
drawboard(board)
let promotion
promotion = document.createElement('div');
promotion.setAttribute('class','promotion');
function fillProm(pieces,move){
  promotion.innerHTML = ''
  pieces.forEach(piece => {
    let x = document.createElement("INPUT");
    x.setAttribute("type", "image");
    x.src = "../static/images/"+piece+".gif";
    x.addEventListener('click',function(e){
      POST(move+piece)
      overlay.classList.remove('overlay')
    });
    
    x.addEventListener('mouseover',function(e){
      let y = document.querySelectorAll('.highlight')
      removehigh(y,'highlight')
      x.classList.add('highlight')
    });
    x.addEventListener('dragstart',function(e){
      e.preventDefault()
    })
    promotion.appendChild(x)
  })
}

let squares = document.querySelectorAll('.square')
squares.forEach(square => {
    square.addEventListener('drop',function(e){
      let move = start + square.id
      if (isLowerCase(beingDragged.id)==colour){
        if (beingDragged.id.toLowerCase()=='k'){
          if(start.substring(0,1)=='e'){
            if(square.id.substring(0,1)=='c'){
              move = 'O-O-O'
            }
            if(square.id.substring(0,1)=='g'){
              move = 'O-O'
            }
          }
        }
        if (legalmoves.includes(move)){
          if(square.children.length != 0){
            if (isLowerCase(e.target.id) != isLowerCase(beingDragged.id)){
              square.textContent = '';
              square.append(beingDragged)
              square.classList.remove('highlight')
              square.classList.remove('highlight2')
            }
          }
          else{
            e.target.append(beingDragged)
            POST(move)
            e.target.classList.remove('highlight')
            square.classList.remove('highlight2')
          }
        }
        else if (legalmoves.includes(move+'P')){
          square.innerHTML = ''
          square.classList.remove('highlight2')
          for (let i = 7; i >4; i--) {
            let s = document.getElementById(square.id.substring(0,1)+i)
            s.innerHTML = ''
          }
          overlay.classList.add('overlay');
          fillProm(['Q','N','B','R'],move)
          square.appendChild(promotion);
        }
        else{
            e.target.classList.remove('highlight')
            square.classList.remove('highlight2')
        }
    }

    });  
    square.addEventListener('dragover',function(e){
      e.preventDefault()
    });  
    square.addEventListener('dragenter',function(e){
      if (isLowerCase(beingDragged.id)==colour)
        if(e.target.tagName =='IMG'){
          if (isLowerCase(e.target.id) != isLowerCase(beingDragged.id)){
            if(e.target.parentNode.classList.contains('target')){
              e.target.parentNode.classList.remove('target')
              e.target.parentNode.classList.add('highlight2')
              setTimeout(()=> e.target.parentNode.classList.add('target'),1000)
            }
            else{
              e.target.parentNode.classList.add('highlight2')
            }
          
          }
        }
        else{
          if(square.children.length == 0){
              e.target.classList.add('highlight')
          }
        }
      });  
    square.addEventListener('dragleave',function(e){
      e.target.classList.remove('highlight')
      e.target.parentNode.classList.remove('highlight2')
    });  
});


