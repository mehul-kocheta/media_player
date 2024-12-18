from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog, QStackedLayout, QGridLayout
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl, QTimer
import subtitles
import save_wav
import whisper


# Create a QWidget-based class to represent the application window
class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties such as title, size, and icon
        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))
        
        
        self.timer = QTimer(self)
        self.timer.setInterval(10)  # Update every second
        self.timer.timeout.connect(self.test)

        # Set window background color
        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        # Initialize the user interface
        self.init_ui()

        # Display the window
        self.show()

    # Initialize the user interface components
    def init_ui(self):
        
        self.sub = 0
        self.subt = subtitles.srt_to_dict()
        self.l = []

        # Create a QMediaPlayer object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Create a QVideoWidget object to display video
        videowidget = QVideoWidget()

        # Create a QPushButton to open video files
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)
        
        subtbtn = QPushButton('Click Here')
        subtbtn.clicked.connect(self.subt_sync)

        # Create a QPushButton to play or pause the video
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # Create a QSlider for seeking within the video
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        # Create a QLabel to display video information or errors
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        
        
        # Create a QHBoxLayout for arranging widgets horizontally
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
        
        
        self.text_label = QLabel()
        self.text_label.setStyleSheet("color: white;")  # Optional styling
        
        subt = QHBoxLayout()
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFixedHeight(50)
        subt.addWidget(self.text_label)


        # Add widgets to the QHBoxLayout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(subtbtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        # Create a QVBoxLayout for arranging widgets vertically
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(subt)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        
        
        # Set the layout of the window
        self.setLayout(vboxLayout)
        
        # Set the video output for the media player
        self.mediaPlayer.setVideoOutput(videowidget)

        # Connect media player signals to their respective slots
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        
        # self.timer.start()

    # Method to open a video file
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.text_label.setText(self.subt[0][2])
            self.playBtn.setEnabled(True)
            
    def subt_sync(self):
        l = self.mediaPlayer.position() - 5000 if self.mediaPlayer.position() - 5000 > 0 else 0
        r = 10000
        self.mediaPlayer.pause()
        self.timer.stop()
        save_wav.extract_audio_by_milliseconds("tbbt.mkv",l,r,"test.wav")
        whisper.save_subt()
        test = subtitles.pysrt.open("test.wav.srt")
        test.shift(milliseconds = self.mediaPlayer.position() - 5000)
        test.save("test.srt")
        self.mediaPlayer.play()
        self.timer.start()

    # Method to play or pause the video
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.timer.stop()
            
        else:
            self.mediaPlayer.play()
            self.timer.start()
            
    def test(self):
        index = self.l[self.mediaPlayer.position()//10]
        if index == -1:
            self.text_label.setText("")
        else:
            self.text_label.setText(self.subt[index][2])

    # Method to handle changes in media player state (playing or paused)
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    # Method to handle changes in video position
    def position_changed(self, position):
        self.slider.setValue(position)
        

    # Method to handle changes in video duration
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        self.l = [-1]*(duration//10 + 1)
        
        for i in range(len(self.subt)):
            for j in range(int(self.subt[i][0]//10), int(self.subt[i][1]//10) + 1):
                self.l[j] = i

    # Method to set the video position
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
        

    # Method to handle errors in media playback
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())

# Create the application instance
app = QApplication(sys.argv)

# Create the main window instance
window = Window()


# Run the application event loop
sys.exit(app.exec_())