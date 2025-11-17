<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<title>Catch the Scorpio</title>
		<style>
			body { background:#111; display:flex; justify-content:center; padding-top:20px; }
			canvas { background:#222; border:3px solid #555; }
		</style>
	</head>
	<body>
		<nav style="width:100%; background:#333; color:white; padding:10px 0; display:flex; justify-content:center; gap:40px; font-family:sans-serif; font-size:18px;">
			<a href="#about" style="color:white; text-decoration:none;">About</a>
			<a href="#location" style="color:white; text-decoration:none;">Location</a>
			<a href="#instructions" style="color:white; text-decoration:none;">Instructions</a>
			<button style="background:#ff4444; color:white; border:none; padding:8px 16px; border-radius:6px; cursor:pointer; font-size:16px;">RSVP</button>
		</nav>

		<canvas id="game" width="600" height="600"></canvas>

		<!-- Player selection -->
		<div id="playerSelect" style="margin-top:20px; width:600px; display:flex; justify-content:center; gap:10px; flex-wrap:wrap;">
			<div class="pOption" data-color="#ff4444" style="width:40px; height:40px; background:#ff4444; cursor:pointer;"></div>
			<div class="pOption" data-color="#44ff44" style="width:40px; height:40px; background:#44ff44; cursor:pointer;"></div>
			<div class="pOption" data-color="#4444ff" style="width:40px; height:40px; background:#4444ff; cursor:pointer;"></div>
			<div class="pOption" data-color="#ffff44" style="width:40px; height:40px; background:#ffff44; cursor:pointer;"></div>
			<div class="pOption" data-color="#ff44ff" style="width:40px; height:40px; background:#ff44ff; cursor:pointer;"></div>
			<div class="pOption" data-color="#44ffff" style="width:40px; height:40px; background:#44ffff; cursor:pointer;"></div>
			<div class="pOption" data-color="#ffffff" style="width:40px; height:40px; background:#ffffff; cursor:pointer; border:1px solid #aaa;"></div>
			<div class="pOption" data-color="#ff8800" style="width:40px; height:40px; background:#ff8800; cursor:pointer;"></div>

			<script>
				const canvas = document.getElementById("game");
				const ctx = canvas.getContext("2d");

				const ROOM_SIZE = 600; // 12ft by 12ft arbitrary scale
				const PLAYER_SIZE = 20;
				const SCORPION_SIZE = 40;
				const HEART_SIZE = 25;

				// Player
				let player = { x:300, y:300, speed:3, color:"cyan" };

				// Heart location (random)
				let heart = randomHeart();

				function randomHeart(){
				  return {
				    x: Math.random()*(ROOM_SIZE-HEART_SIZE),
				    y: Math.random()*(ROOM_SIZE-HEART_SIZE)
				  };
				}

				// Smooth scorpion movement
				let scorpion = {
				  x: Math.random()*ROOM_SIZE,
				  y: Math.random()*ROOM_SIZE,
				  targetX: Math.random()*ROOM_SIZE,
				  targetY: Math.random()*ROOM_SIZE,
				  speed: 0.5,
				  img: null
				};

				// Load scorpion image
				scorpion.img = new Image();
				scorpion.img.src = "Image.png";

				let keys = {};

				document.addEventListener("keydown", e => keys[e.key] = true);
				document.addEventListener("keyup", e => keys[e.key] = false);

				function movePlayer(){
				  if (keys["ArrowUp"]) player.y -= player.speed;
				  if (keys["ArrowDown"]) player.y += player.speed;
				  if (keys["ArrowLeft"]) player.x -= player.speed;
				  if (keys["ArrowRight"]) player.x += player.speed;

				  // keep inside room
				  player.x = Math.max(0, Math.min(ROOM_SIZE-PLAYER_SIZE, player.x));
				  player.y = Math.max(0, Math.min(ROOM_SIZE-PLAYER_SIZE, player.y));
				}

				function moveScorpion(){
				  // pick new target when close
				  let dx = scorpion.targetX - scorpion.x;
				  let dy = scorpion.targetY - scorpion.y;
				  let dist = Math.hypot(dx, dy);
				  if (dist < 10){
				    scorpion.targetX = Math.random()*ROOM_SIZE;
				    scorpion.targetY = Math.random()*ROOM_SIZE;
				  }

				  // smooth movement
				  scorpion.x += (dx/dist) * scorpion.speed;
				  scorpion.y += (dy/dist) * scorpion.speed;
				}

				function draw(){
				  ctx.clearRect(0,0,ROOM_SIZE,ROOM_SIZE);

				  // Draw heart
				  ctx.fillStyle = "red";
				  ctx.fillRect(heart.x, heart.y, HEART_SIZE, HEART_SIZE);

				  // Draw player
				  ctx.fillStyle = player.color;
				  ctx.fillRect(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE);

				  // Draw scorpion image
				  if (scorpion.img.complete){
				    ctx.drawImage(scorpion.img, scorpion.x, scorpion.y, SCORPION_SIZE, SCORPION_SIZE);
				  } else {
				    ctx.fillStyle = "yellow";
				    ctx.fillRect(scorpion.x, scorpion.y, SCORPION_SIZE, SCORPION_SIZE);
				  }
				}

				function checkCollisions(){
				  // Player gets heart
				  if (rectOverlap(player, PLAYER_SIZE, heart, HEART_SIZE)){
				    alert("You collected the heart! You win! Restarting...");
				    resetGame();
				  }

				  // Scorpion hits player
				  if (rectOverlap(player, PLAYER_SIZE, scorpion, SCORPION_SIZE)){
				    alert("Stung! You must choose: join someone else OR outperform someone. Restarting...");
				    resetGame();
				  }
				}

				function rectOverlap(a, sizeA, b, sizeB){
				  return !(a.x+sizeA < b.x || a.x > b.x+sizeB || a.y+sizeA < b.y || a.y > b.y+sizeB);
				}

				function resetGame(){
				  player = { x:300, y:300, speed:3 };
				  scorpion.x = Math.random()*ROOM_SIZE;
				  scorpion.y = Math.random()*ROOM_SIZE;
				  scorpion.targetX = Math.random()*ROOM_SIZE;
				  scorpion.targetY = Math.random()*ROOM_SIZE;
				  heart = randomHeart();
				}

				// Player color selection logic
				document.querySelectorAll('.pOption').forEach(opt => {
				  opt.addEventListener('click', () => {
				    player.color = opt.dataset.color;
				  });
				});

				function loop(){
				  movePlayer();
				  moveScorpion();
				  draw();
				  checkCollisions();
				  requestAnimationFrame(loop);
				}

				loop();
			</script>
		</div>
	</body>
</html>
