class ConvClassifier(nn.Module):
    
    def __init__(self, n_classes):
        super().__init__()
        
        self.Convs = nn.Sequential()
        
        self.ConvBlock1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1), nn.LeakyReLU(),
            nn.Conv2d(32, 32, kernel_size=3, padding=1), nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Dropout2d(p=0.25)
        )
        
        self.ConvBlock2 = nn.Sequential(
            nn.Conv2d(32, 128, kernel_size=3, padding=1), nn.LeakyReLU(),
            nn.Conv2d(128, 128, kernel_size=5, padding=2), nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Dropout2d(p=0.25)
        )
        
        self.ConvBlock2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.LeakyReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1), nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Dropout2d(p=0.25)
        )
        
        self.fc1 = nn.Linear(1*28*28+32*14*14, 256)
        self.fc2 = nn.Linear(1*28*28+64*7*7, 256)
        
        self.out = nn.Sequential(
            nn.Linear(512, 128), nn.ReLU(),
            nn.Linear(128, 32), nn.ReLU(),
            nn.Linear(32, n_classes)
        )
        
        self.loss = nn.CrossEntropyLoss()
        
    def forward(self, x, label=False):
        logits = self._inference(x)
        if label is not False:
            loss = self.loss(logits, label)
            return (logits, loss)
        return logits
        
    def _inference(self, x):
        bsz = x.size(0)
        conv1 = self.ConvBlock1(x)
        conv2 = self.ConvBlock2(conv1)
        
        # Flatten
        x = x.view(bsz, -1)
        conv1 = conv1.view(bsz, -1)
        conv2 = conv2.view(bsz, -1)
        # Concat
        x1 = torch.cat([x, conv1], dim=1)
        x2 = torch.cat([x, conv2], dim=1)
        
        fc_out_1 = self.fc1(x1)
        fc_out_2 = self.fc2(x2)
        
        # Concat
        fc_out = torch.cat([fc_out_1, fc_out_2], dim=1)
        
        logits = F.softmax(self.out(fc_out), dim=1)
        
        return logits
