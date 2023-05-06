for bx in range(630, 1100, 70):
        boxes.add(Box(bx, 1000))
    for bx in range(0, 90, 70):
        boxes.add(Box(bx, 1000))
    for bx in range(210, 400, 70):
        boxes.add(Box(bx, 1000))
    for bx in range(0, 980, 70):
        boxes.add(Box(bx, 790))
    for bx in range(420, 600, 70):
        boxes.add(Box(bx, 720))
    for bx in range(840, 1100, 70):
        boxes.add(Box(bx, 720))
    for bx in range(0, 560, 70):
        boxes.add(Box(bx, 550))
    for bx in range(0, 80, 70):
        boxes.add(Box(bx, 340))
    for bx in range(310, 1150, 70):
        boxes.add(Box(bx, 290))
    for bx in range(1050, 1120, 70):
        boxes.add(Box(bx, 220))
    for bx in range(1050, 1120, 70):
        boxes.add(Box(bx, 150))
    for bx in range(0, 1120, 70):
        boxes.add(Box(bx, 80))
    for bx in range(69, 70, 70):
        boxes.add(Box(bx, 480))

     # лава
    # lavas = pygame.sprite.Group()
    # for bx in range(140, 190, 70):
    #     lavas.add(Lava(bx, 1000))
    # for bx in range(420, 600, 70):
    #     lavas.add(Lava(bx, 1000))
    # for bx in range(630, 800, 70):
    #     lavas.add(Lava(bx, 725))
    # for bx in range(139, 140, 70):
    #     lavas.add(Lava(bx, 415))

    #тест ЛАВАшки
    lava = Lava(140, 415)
    lava1 = Lava(631, 720)
    lava2 = Lava(700, 720)
    lava3 = Lava(770, 720)
    lava4 = Lava(421, 1000)
    lava5 = Lava(491, 1000)
    lava6 = Lava(561, 1000)
    lava7 = Lava(140, 1000)

    # лестница
    for bx in range(280, 350, 70):
        boxes.add(Box(bx, 930))
    for bx in range(280, 350, 70):
        boxes.add(Box(bx, 860))
    for bx in range(139, 140, 70):
        boxes.add(Box(bx, 480))
    for bx in range(69, 70, 70):
        boxes.add(Box(bx, 410))
