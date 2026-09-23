'use strict';

var gameStart = {};
var gameSpeed = {};
var gameArea = {};
var gameAreaContext = {};
var snake = [];
var gameAreaWidth = 0;
var gameAreaHeight = 0;
var cellWidth = 0;
var playerScore = 0;
var snakeFood = {};
var snakeDirection = '';
var speedSize = 0;
var timer = {};

const CLAIM_URL = '/api/claim';
const SIGNING_SALT = 'HCS{coba_submit_flag_ini_siapa_tau_bukan_decoy_xixixi}';
let seed = 0;
let serverScore = 0;
let integrity = 0;
let eats = 0;

function initElement() {
  gameStart = document.querySelector("#gameStart");
  gameSpeed = document.querySelector("#gameSpeed");
  gameArea = document.querySelector('#gameArea');
  gameAreaContext = gameArea.getContext('2d');
  gameAreaWidth = 400;
  gameAreaHeight = 600;
  cellWidth = 20;
  gameArea.width = gameAreaWidth;
  gameArea.height = gameAreaHeight;
}

function createFood() {
  snakeFood = {
    'x': Math.round(Math.random() * (gameAreaWidth - cellWidth) / cellWidth),
    'y': Math.round(Math.random() * (gameAreaHeight - cellWidth) / cellWidth)
  };
}

function checkCollision(x, y, array) {
  for (let i = 0; i < array.length; i++) {
    if (array[i].x == x && array[i].y == y) {
      return true;
    }
  }
  return false;
}

function writeScore() {
  gameAreaContext.font = "20px sans-serif";
  gameAreaContext.fillStyle = "#0000FF";
  gameAreaContext.fillText("Score: " + playerScore, 20, 25);
}

function createSquare(x, y) {
  gameAreaContext.fillStyle = "#000000";
  gameAreaContext.fillRect(x * cellWidth, y * cellWidth, cellWidth, cellWidth);
}

function updateOnEat() {
  eats++;
  serverScore += 9;
  integrity = ((((integrity << 5) | (integrity >>> 27)) ^ (seed + serverScore)) >>> 0);
}

function drawResult(text) {
  gameAreaContext.fillStyle = '#ff0000';
  gameAreaContext.font = "20px sans-serif";
  gameAreaContext.textAlign = "center";
  gameAreaContext.fillText(text, gameAreaWidth / 2, gameAreaHeight / 2);
}

async function submitRun() {
  const payload = {};
  payload['score'] = serverScore;
  payload['eats'] = eats;
  payload['integrity'] = integrity;
  const sigInput = `${payload.score}|${payload.eats}|${payload.integrity}|${SIGNING_SALT}`;
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(sigInput));
  payload.sig = Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
  try {
    const res = await fetch(CLAIM_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    drawResult(data.flag || data.msg);
  } catch (e) {
    drawResult('Could not reach backend. Contact problem setter');
  }
}

function createGameArea() {
  let newHeadX = snake[0].x;
  let newHeadY = snake[0].y;

  gameAreaContext.fillStyle = '#FFFFFF';
  gameAreaContext.fillRect(0, 0, gameAreaWidth, gameAreaHeight);
  gameAreaContext.strokeStyle = '#000000';
  gameAreaContext.strokeRect(0, 0, gameAreaWidth, gameAreaHeight);

  writeScore();

  if (snakeDirection == "right") newHeadX++;
  else if (snakeDirection == "left") newHeadX--;
  else if (snakeDirection == "down") newHeadY++;
  else if (snakeDirection == 'up') newHeadY--;

  if (newHeadX == -1 || newHeadX == gameAreaWidth / cellWidth || newHeadY == -1 || newHeadY == gameAreaHeight / cellWidth || checkCollision(newHeadX, newHeadY, snake)) {
    clearInterval(timer);
    gameStart.disabled = false;
    submitRun();
    return;
  }

  let newHead = { 'x': newHeadX, 'y': newHeadY };

  if (newHeadX == snakeFood.x && newHeadY == snakeFood.y) {
    playerScore += speedSize;
    updateOnEat();
    createFood();
  } else {
    snake.pop();
  }

  snake.unshift(newHead);

  for (let i = 0; i < snake.length; i++) {
    createSquare(snake[i].x, snake[i].y);
  }
  createSquare(snakeFood.x, snakeFood.y);
}

function startGame() {
  seed = gameAreaWidth * 10000 + gameAreaHeight;
  serverScore = 0;
  integrity = seed;
  eats = 0;
  snake = [{ 'x': 5, 'y': 5 }];
  createFood();
  clearInterval(timer);
  timer = setInterval(createGameArea, 500 / speedSize);
}

function onStartGame() {
  this.disabled = true;
  playerScore = 0;
  snakeDirection = "right";
  speedSize = parseInt(gameSpeed.value);
  if (speedSize > 9) speedSize = 9;
  else if (speedSize < 1) speedSize = 1;
  startGame();
}

function changeDirection(event) {
  const keyCode = event.which;
  if (keyCode == '40' && snakeDirection != 'up') snakeDirection = "down";
  else if (keyCode == '39' && snakeDirection != 'left') snakeDirection = 'right';
  else if (keyCode == '38' && snakeDirection != "down") snakeDirection = 'up';
  else if (keyCode == '37' && snakeDirection != 'right') snakeDirection = "left";
}

function initEvent() {
  gameStart.addEventListener("click", onStartGame);
  window.addEventListener("keydown", changeDirection);
}

function init() {
  initElement();
  initEvent();
}

window.addEventListener("DOMContentLoaded", init);
