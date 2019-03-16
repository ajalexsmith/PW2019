class Settings:
    def __init__(self):
        SettingsFile = open("Settings.txt", "r")

        r = str(SettingsFile.readline())
        g = str(SettingsFile.readline())
        b = str(SettingsFile.readline())
        nebRed = str(SettingsFile.readline())
        nebBlu = str(SettingsFile.readline())
        nebYel = str(SettingsFile.readline())
        nebGre = str(SettingsFile.readline())

        self.blR = r.replace('\n', '')
        self.blG = g.replace('\n', '')
        self.blB = b.replace('\n', '')
        self.nebRed = nebRed.replace('\n', '')
        self.nebBlue = nebBlu.replace('\n', '')
        self.nebYellow = nebYel.replace('\n', '')
        self.nebGreen = nebGre.replace('\n', '')

    def saveSettings(self):
        SettingsFile = open("Settings.txt", "w")
        SettingsFile.write((str(self.blR) + '\n' + str(self.blG) + '\n' + str(self.blB) + '\n' + str(self.nebRed) + '\n' + str(self.nebBlue) + '\n' + str(self.nebYellow) + '\n' + str(self.nebGreen)))
        SettingsFile.close()

