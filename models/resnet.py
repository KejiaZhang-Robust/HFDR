import torch

from .utils import *
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class PreActBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(PreActBlock, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes)
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)

        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False)
            )

    def forward(self, x):
        out = F.relu(self.bn1(x))
        shortcut = self.shortcut(out) if hasattr(self, 'shortcut') else x
        out = self.conv1(out)
        out = self.conv2(F.relu(self.bn2(out)))
        out += shortcut
        return out


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion*planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion*planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10, norm = False, mean = None, std = None):
        super(ResNet, self).__init__()
        self.in_planes = 64
        self.norm = norm
        self.mean = mean
        self.std = std

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.linear = nn.Linear(512*block.expansion, num_classes)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        if self.norm == True:
            x = Normalization(x, self.mean, self.std)
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out

def PreActResNet18(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet(PreActBlock, [2,2,2,2], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)

def ResNet18(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet(BasicBlock, [2,2,2,2], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)

def ResNet34(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet(BasicBlock, [3,4,6,3], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)

def ResNet50(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet(Bottleneck, [3,4,6,3], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)

def ResNet101(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet(Bottleneck, [3,4,23,3], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)

def ResNet152(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet(Bottleneck, [3,8,36,3], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)

class ResNet_F(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10, norm = False, mean = None, std = None):
        super(ResNet_F, self).__init__()
        self.in_planes = 64
        self.norm = norm
        self.mean = mean
        self.std = std

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.linear = nn.Linear(512*block.expansion, num_classes)
        self.recon_size = 64
        self.Filter = SRMFilter(self.recon_size)
        self.Recon = Recalibration(self.recon_size)
        self.C_HF = nn.Linear(self.recon_size, 10)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x, is_eval=False):
        if self.norm == True:
            x = Normalization(x, self.mean, self.std)
        out = F.relu(self.bn1(self.conv1(x)))
        HF, LF, mask = self.Filter(out)
        HF_fine = self.Recon(HF, mask)
        out = (HF_fine) + LF
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out_1 = self.linear(out)
        if is_eval == False:
            return out_1
        else:
            return out_1, mask

def PreActResNet18_F(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet_F(PreActBlock, [2,2,2,2], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)

def ResNet18_F(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet_F(BasicBlock, [2,2,2,2], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)


class ResNet_DFT(nn.Module):
    def __init__(self, block, num_blocks, num_classes=10, norm = False, mean = None, std = None):
        super(ResNet_DFT, self).__init__()
        self.in_planes = 64
        self.norm = norm
        self.mean = mean
        self.std = std

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.linear = nn.Linear(512*block.expansion, num_classes)
        self.recon_size = 64
        self.Filter = DFT_high_pass(8)
        self.Recon = Recalibration(self.recon_size)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x, is_eval=False):
        if self.norm == True:
            x = Normalization(x, self.mean, self.std)
        out = F.relu(self.bn1(self.conv1(x)))
        HF, LF, mask = self.Filter(out)
        HF_fine = self.Recon(HF, mask)
        out = (HF_fine) + LF
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out_1 = self.linear(out)
        if is_eval == False:
            return out_1
        else:
            return out_1, mask
        
def ResNet18_DFT_F(Num_class=10, Norm=False, norm_mean=None, norm_std=None):
    return ResNet_DFT(BasicBlock, [2,2,2,2], num_classes=Num_class, norm=Norm, mean=norm_mean, std=norm_std)
