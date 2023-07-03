import turtle
import mesa
import random
import tkinter.messagebox

from utils.calcula_disntacia import distance


ID = 4
RANGE = 5
TAMANHO_MAPA = 160
COORD_INICIO = (-170, 180)
COORD_CIVIL = (150, -180)
COOR_CENTER = (0, 0)
COORD_SAIDA = (160, 180)
MAPA_JOGAVEL_X = 160
MAPA_JOGAVEL_Y = 60

MONSTRO_GIF = [
    'gifs/minotaur_default.gif',
    'gifs/goblin_default.gif'
]

PESSOA_GIF = 'gifs/boneco_normal.gif'
HEROI_GIF = 'gifs/hero_default.gif'


window = tkinter.Tk()
canvas = tkinter.Canvas(master=window, width=400, height=400)
canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10)
screen = turtle.TurtleScreen(canvas)
screen.bgpic('gifs/background_florest.png')
screen.register_shape(PESSOA_GIF)
screen.register_shape('gifs/hero_default.gif')
for gif in MONSTRO_GIF:
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
        self.shape.hideturtle()
        self.escondido = True


class Heroi(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.x = 0
        self.y = 60
        self.vida = random.randint(0, 150)
        createShade(self, 'gifs/hero_default.gif')

    def move(self):
        self.resgatar()

    def morte(self):
        self.shape.hideturtle()
        self.escondido = True

    def atacar(self):
        self.shape.shape('gifs/boneco_cansado.gif')

    def resgatar(self):
        pessoasNaoSalvas = balada.pessoas_nao_salvas()
        if (len(pessoasNaoSalvas) == 0):
            return

        indexRnd = random.randint(0, len(pessoasNaoSalvas) - 1)

        pessoaRegate = pessoasNaoSalvas[indexRnd]

        self.shape.goto(pessoaRegate.x, pessoaRegate.y)
        self.shape.goto(COORD_SAIDA)
        pessoaRegate.resgate()


class Pessoa(Agente):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        createShade(self, 'gifs/boneco_normal.gif')
        self.salvo = False
        self.morto = False

    def move(self):
        if (self.salvo):
            return

        if (self.vida <= 0):
            self.morte()
        elif (game.verifica_monstros_perto(self)):
            self.vida -= 1

    def morte(self):
        self.shape.hideturtle()
        self.morto = True
        self.escondido = True

    def resgate(self):
        if (game.verifica_monstros_perto(self)):
            return

        self.shape.goto(COORD_SAIDA)
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
            self.pessoas.append(p)
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
        self.monstros.append(m)
        self.schedule.add(m)

    def verifica_monstros_perto(self, agent):
        monstros = game.monstros
        for monstro in monstros:
            if (self.esta_perto(monstro, agent)):
                return 1
        return 0

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
    master=window, text="Check todo mundo", command=game.remover_pessoa)
Play_Button.config(bg="light gray", fg="black")
Board_Button.grid(padx=2, pady=2, row=1, column=11, sticky='nsew')

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
