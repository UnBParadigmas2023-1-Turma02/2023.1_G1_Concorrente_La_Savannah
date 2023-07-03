import turtle
import mesa
import time
import random
import tkinter.messagebox

from utils.calcula_disntacia import distance


ID = 4
RANGE = 5
TAMANHO_MAPA = 160
COORD_INICIO = (-170, 180)
COORD_CIVIL = (150, -180)
COOR_CENTER = (0, 0)
COORD_SAIDA = (0, 60)
COORD_SAIDA_X = 0
COORD_SAIDA_Y = 60
MAPA_JOGAVEL_X = 160
MAPA_JOGAVEL_Y = 60

MONSTRO_GIF = [
    'gifs/minotaur_default.gif',
    'gifs/goblin_default.gif'
]

MONSTRO_DIE_GIF = [
    'gifs/minotaur_die.gif',
    'gifs/goblin_default.gif'
]

PESSOA_GIF = ['gifs/boneco_normal.gif', 'gifs/boneco_curtindo.gif']
HEROI_GIF = 'gifs/hero_default.gif'
HEROI_ATAQUE_GIF = 'gifs/hero_atack.gif'


window = tkinter.Tk()
canvas = tkinter.Canvas(master=window, width=400, height=400)
canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10)
screen = turtle.TurtleScreen(canvas)
screen.bgpic('gifs/background_florest.png')
screen.register_shape(HEROI_ATAQUE_GIF)
screen.register_shape(HEROI_GIF)
for gif in MONSTRO_DIE_GIF:
    screen.register_shape(gif)
for gif in MONSTRO_GIF:
    screen.register_shape(gif)
for gif in PESSOA_GIF:
    screen.register_shape(gif)


def createShade(self, url):
    self.shape = turtle.RawTurtle(screen)
    self.shape.hideturtle()
    self.shape.shape(url)
    self.shape.penup()
    self.shape.setposition(self.x, self.y)
    self.shape.showturtle()


class Agente(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.x = random.randint(-TAMANHO_MAPA, MAPA_JOGAVEL_X)
        self.y = random.randint(-TAMANHO_MAPA, MAPA_JOGAVEL_Y)
        self.vida = random.randint(0, 150)
        self.escondido = False


class Monstro(Agente):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.monsterId = random.randint(0, len(MONSTRO_GIF) - 1)
        createShade(self, MONSTRO_GIF[self.monsterId])

    def move(self):
        if (self.vida == 0):
            self.morrer()
        else:
            self.walk_monster()

    def walk_monster(self):
        # Lógica para andar aleatoriamente pelo mapa
        dx = random.randint(-10, 10)
        dy = random.randint(-30, 30)

        # Adicionando um fator de aleatoriedade para a direção dos movimentos
        dx *= random.choice([-1, 1])
        dy *= random.choice([-1, 1])

        self.x += dx
        self.y += dy

        # Limitando as coordenadas para que o boneco permaneça dentro dos limites do mapa
        self.x = max(min(self.x, MAPA_JOGAVEL_X), -TAMANHO_MAPA)
        self.y = max(min(self.y, MAPA_JOGAVEL_Y), -TAMANHO_MAPA)

        self.shape.goto(self.x, self.y)

    def morrer(self):
        self.shape.shape(MONSTRO_DIE_GIF[0])
        time.sleep(0.2)
        self.escondido = True
        self.vida = 0
        self.shape.hideturtle()


class Heroi(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.x = 0
        self.y = 60
        self.vida = random.randint(0, 150)
        self.alvoResgate = None
        createShade(self, 'gifs/hero_default.gif')

    def move(self):
        pessoas_vivas = game.pessoas_vivas()
        monstros_vivos = game.monstros_vivos()

        if (len(pessoas_vivas) >= 1):
            self.resgatar()
        elif (len(monstros_vivos) >= 1):
            self.cacar_monstro(monstros_vivos)

    def cacar_monstro(self, monstros):
        index = random.randint(0, len(monstros) - 1)
        alvo = monstros[index]
        self.ataca_monstro(alvo)

    def morte(self):
        self.shape.hideturtle()
        self.escondido = True

    def escolhe_alvo_resgate(self):
        if (self.alvoResgate and (not self.alvoResgate.salvo and not self.alvoResgate.morto)):
            return
        else:
            pessoasNaoSalvas = game.pessoas_vivas()
            if (len(pessoasNaoSalvas) == 0):
                return
            indexRnd = random.randint(0, len(pessoasNaoSalvas) - 1)
            self.alvoResgate = pessoasNaoSalvas[indexRnd]

    def resgatar(self):
        self.escolhe_alvo_resgate()

        self.shape.goto(self.alvoResgate.x - 10, self.alvoResgate.y - 10)

        monstros_perto_alvo = game.verifica_monstros_perto(self.alvoResgate)

        if (len(monstros_perto_alvo) == 0):
            self.alvoResgate.resgate()
            self.shape.goto(COORD_SAIDA)
        else:
            self.cacar_monstro(monstros_perto_alvo)

    def ataca_monstro(self, monstro):
        self.shape.goto(monstro.x - 20, monstro.y - 10)
        self.shape.shape('gifs/hero_atack.gif')
        time.sleep(0.2)
        monstro.morrer()
        self.shape.shape('gifs/hero_default.gif')


class Pessoa(Agente):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        createShade(self, 'gifs/boneco_normal.gif')
        self.id = unique_id
        self.salvo = False
        self.morto = False

    def move(self):
        if (self.salvo):
            return

        if (self.vida <= 0):
            self.morte()
        elif (len(game.verifica_monstros_perto(self)) >= 1):
            self.vida -= 1

    def morte(self):
        self.shape.hideturtle()
        self.morto = True
        self.escondido = True

    def resgate(self):
        if (len(game.verifica_monstros_perto(self)) >= 1):
            return

        valor_variavel = 2 * random.randint(-self.id, self.id)
        self.shape.goto(COORD_SAIDA_X + valor_variavel, COORD_SAIDA_Y)
        self.shape.shape('gifs/boneco_curtindo.gif')
        self.escondido = True
        self.salvo = True

    def backtoinitialpoint(self):
        x, y = self.shape.position()
        xs, ys = COORD_INICIO

        if x > xs:
            self.x -= 5
        if y < ys:
            self.y += 5

        if x <= 0 and y >= 0:  # REVER ISSO AQUI
            self.centro = 0

        self.shape.goto(self.x, self.y)

    def gotocenter(self):
        x, y = self.shape.position()
        xs, ys = COOR_CENTER

        if x < xs:
            self.x += 5
        if y > ys:
            self.y -= 5

        if x >= 0 and y <= 0:
            self.centro = 0

        self.shape.goto(self.x, self.y)

    def gotocivil(self):
        x, y = self.shape.position()
        xs, ys = COORD_CIVIL

        if x < xs:
            self.x += 5
        if y > ys:
            self.y -= 5

        if (x >= 150 and y <= -180):
            self.energiaHeroi += random.randint(1, 10)
            self.isRescued = True

            self.centro = random.randint(0, 3)

        self.shape.goto(self.x, self.y)

    def gotosaida(self):
        x, y = self.shape.position()
        xs, ys = COORD_INICIO

        if x < xs:
            self.x += 5
        if y < ys:
            self.y += 5

        if (x >= 160 and y >= 180):
            self.shape.hideturtle()
            if (not self.escondido):
                self.escondido = True

        self.shape.goto(self.x, self.y)


class GameModel(mesa.Model):
    def __init__(self, N):
        self.num_monstros = N
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.pessoas = []
        self.monstros = []
        self.herois = []
        self.id = 10

        for i in range(self.num_monstros):
            p = Monstro(i, self)
            self.monstros.append(p)
            self.schedule.add(p)
            self.id += 1

    def step(self):
        for pessoa in self.schedule.agents:
            pessoa.move()
            if (pessoa.shape.position == COORD_SAIDA):
                self.schedule.remove(pessoa)

    def numero_pessoas(self):
        print(self.schedule.get_agent_count())

    def remover_pessoa(self):
        for i in self.pessoas:
            i.mostra_status()

    def adicionar_heroi(self):
        a = Heroi(self.id, self)
        self.id += 1
        self.herois.append(a)
        self.schedule.add(a)

    def adicionar_monstro(self):
        m = Monstro(self.id, self)
        self.id += 1
        self.monstros.append(m)
        self.schedule.add(m)

    def adicionar_pessoa(self):
        m = Pessoa(self.id, self)
        self.id += 1
        self.pessoas.append(m)
        self.schedule.add(m)

    def verifica_monstros_perto(self, agent):
        monstros = game.monstros
        monstros_perto = []
        for monstro in monstros:
            if (self.esta_perto(monstro, agent) and monstro.vida > 0):
                monstros_perto.append(monstro)

        return monstros_perto

    def pessoas_vivas(self):
        vivos = []
        for pessoa in self.pessoas:
            if (not pessoa.salvo and not pessoa.morto):
                vivos.append(pessoa)
        return vivos

    def monstros_vivos(self):
        vivos = []
        for monstro in self.monstros:
            if (monstro.vida >= 1 and not monstro.escondido):
                vivos.append(monstro)
        return vivos

    def esta_perto(self, primeiro, segundo):
        distanciaAceitaComoPerto = range(-50, 50)
        distanciaX = primeiro.x - segundo.x
        distanciaY = primeiro.y - segundo.y

        return distanciaX in distanciaAceitaComoPerto and distanciaY in distanciaAceitaComoPerto

    def next_agent_id(self):
        return max([agent.unique_id for agent in self.schedule.agents]) + 1


def escreverLog(mensagem):
    log = open("utils/log.txt", "a")
    log.write(f"{mensagem}\n")
    log.close()


FLAG = True

# Test Tkinker
global game
game = GameModel(10)


def Play():
    # mixer.music.play()
    while FLAG:
        game.step()


Play_Button = tkinter.Button(
    master=window, text="Iniciar simulação", command=Play)
Play_Button.config(bg="light gray", fg="black")
Play_Button.grid(padx=2, pady=2, row=0, column=11, sticky='nsew')

Board_Button = tkinter.Button(
    master=window, text="Adicionar Heróis", command=game.adicionar_heroi)
Play_Button.config(bg="light gray", fg="black")
Board_Button.grid(padx=2, pady=2, row=2, column=11, sticky='nsew')

Board_Button = tkinter.Button(
    master=window, text="Adicionar Monstros", command=game.adicionar_monstro)
Play_Button.config(bg="light gray", fg="black")
Board_Button.grid(padx=2, pady=2, row=3, column=11, sticky='nsew')

Board_Button = tkinter.Button(
    master=window, text="Adicionar Pessoas para resgate", command=game.adicionar_pessoa)
Play_Button.config(bg="light gray", fg="black")
Board_Button.grid(padx=2, pady=2, row=4, column=11, sticky='nsew')
window.mainloop()
