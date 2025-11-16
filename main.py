import pyxel
import time


class Player:
    def __init__(self, x=0, y=112):
        """プレイヤー初期化"""
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.vy = 0  # 垂直速度
        self.is_jumping = False

    def update(self):
        """移動処理 + ジャンプ + 重力"""
        # 左右移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + 2, 160)

        # ジャンプ処理（地面にいる時のみ）
        if not self.is_jumping and pyxel.btnp(pyxel.KEY_SPACE):
            self.vy = -3.5  # 上方向へ初速度
            self.is_jumping = True

        # 重力を加える
        self.vy += 0.3
        self.y += self.vy

        # 地面の高さに着地
        if self.y > 112:
            self.y = 112
            self.vy = 0
            self.is_jumping = False

    def draw(self):
        """描画"""
        pyxel.blt(self.x, self.y, 0, 8, 8, self.w, self.h, 7)


class Enemy:
    def __init__(self, x, y, u=8, v=0, w=8, h=8, colkey=7, move_range=10, speed=0.8):
        """敵キャラの初期化"""
        self.start_x = x
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.colkey = colkey
        self.move_range = move_range
        self.speed = speed
        self.dir = 1  # 1:右, -1:左

    def update(self):
        """左右に往復移動"""
        self.x += self.dir * self.speed
        if self.x > self.start_x + self.move_range or self.x < self.start_x - self.move_range:
            self.dir *= -1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h, self.colkey)


class Item:
    def __init__(self, x=150, y=100):
        """アイテム初期化"""
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h, 7)


class App:
    def __init__(self):
        pyxel.init(164, 128, title="Pyxel Action Ninja Game")
        pyxel.load("my_resource.pyxres")

        self.state = "start"
        self.start_time = 0.0
        self.elapsed_sec = 0.0

        self.player = Player()
        self.enemies = [
            Enemy(100, 112),
            Enemy(48, 112, move_range=35),
            Enemy(128, 112, move_range=15),
        ]
        self.item = Item()

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """ゲームを初期状態に戻す"""
        self.state = "start"
        self.player = Player()
        self.enemies = [
            Enemy(100, 112),
            Enemy(48, 112, move_range=35),
            Enemy(128, 112, move_range=15),
        ]
        self.item = Item()

    def check_collision(self, a, b):
        """矩形同士の当たり判定"""
        return (
            a.x < b.x + b.w and
            a.x + a.w > b.x and
            a.y < b.y + b.h and
            a.y + a.h > b.y
        )

    def update(self):
        # --- スタート画面 ---
        if self.state == "start":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "game"
                self.start_time = time.time()

        # --- ゲーム画面 ---
        elif self.state == "game":
            if pyxel.btnp(pyxel.KEY_Q):
                self.reset_game()
                return

            self.player.update()

            # 敵との当たり判定
            for e in self.enemies:
                e.update()
                if self.check_collision(self.player, e):
                    self.state = "over"
                    return

            # アイテムとの当たり判定（ここを追加！）
            if self.check_collision(self.player, self.item):
                self.state = "clear"
                return

            # 経過時間
            self.elapsed_sec = time.time() - self.start_time

            # 時間制限でゲームオーバー
            if self.elapsed_sec >= 30:
                self.state = "over"

        # --- ゲームオーバー画面 ---
        elif self.state == "over":
            if pyxel.btnp(pyxel.KEY_Q):
                self.reset_game()

        # --- クリア画面 ---
        elif self.state == "clear":
            if pyxel.btnp(pyxel.KEY_Q):
                self.reset_game()

    def draw(self):
        pyxel.cls(0)

        if self.state == "start":
            pyxel.text(40, 40, "PYXEL ACTION NINJA GAME", 7)
            pyxel.text(45, 60, "PRESS SPACE TO START", 10)

        elif self.state == "game":
            pyxel.bltm(0, 0, 0, 0, 0, 164, 128)
            self.player.draw()
            for e in self.enemies:
                e.draw()
            self.item.draw()
            pyxel.text(5, 5, f"TIME: {self.elapsed_sec:05.1f}", 7)

        elif self.state == "over":
            pyxel.text(60, 50, "GAME OVER", 10)
            pyxel.text(45, 70, "PRESS Q TO RESTART", 7)

        elif self.state == "clear":
            pyxel.text(60, 50, "GAME CLEAR", 11)
            pyxel.text(45, 70, "PRESS Q TO RESTART", 7)


App()
