import torch
import torch.nn as nn


def conv_bn_relu_maxp(in_channels, out_channels, ks):
    return [nn.Conv2d(in_channels, out_channels,
                      kernel_size=ks,
                      stride=1,
                      padding=int((ks-1)/2), bias=False),
            nn.Conv2d(out_channels, out_channels,
                      kernel_size=ks,
                      stride=1,
                      padding=int((ks-1)/2), bias=False),
            nn.Conv2d(out_channels, out_channels,
                      kernel_size=ks,
                      stride=1,
                      padding=int((ks-1)/2), bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2)]


class Linear(nn.Module):

    def __init__(self, input_dim, num_classes):
        super(Linear, self).__init__()

        self.classifier = nn.Linear(input_dim[0]*input_dim[1]*input_dim[2], num_classes)

    def forward(self, inputs):
        inputs = inputs.view(inputs.shape[0], -1)
        return self.classifier(inputs)


class CNN(nn.Module):

    def __init__(self, input_dim, num_classes, use_dropout):
        super(CNN, self).__init__()

        layers = conv_bn_relu_maxp(3, 64, 3)\
                +conv_bn_relu_maxp(64, 128, 3)\
                +conv_bn_relu_maxp(128, 256, 3)

        if use_dropout:
            self.features = nn.Sequential(*layers, nn.Dropout(0.5))
        else:
            self.features = nn.Sequential(*layers)

        probe_tensor = torch.zeros((1,) + input_dim)
        features = self.features(probe_tensor)
        print("Feature maps size : {}".format(features.shape))
        features_dim = features.view(-1)

        self.classifier = nn.Linear(features_dim.shape[0], num_classes)


    def forward(self, inputs):
        features = self.features(inputs)
        features = features.view(features.size()[0], -1)
        return self.classifier(features)


def conv_relu_bn(c_in, c_out, ks):
    return [nn.Conv2d(c_in, c_out,
                      kernel_size=ks,
                      stride=1,
                      padding=int((ks-1)/2), bias=False),
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(c_out)]



def bn_relu_conv(c_in, c_out, ks):
    return [nn.BatchNorm2d(c_in),
            nn.ReLU(inplace=True),
            nn.Conv2d(c_in, c_out,
                      kernel_size=ks,
                      stride=1,
                      padding=int((ks-1)/2), bias=False)]



class WRN_Block(nn.Module):

    def __init__(self, c_in, c_out, use_dropout):
        super(WRN_Block, self).__init__()

        if use_dropout:
            #self.c33 = nn.Sequential(
            #        *bn_relu_conv(c_in, c_out, 3),
            #        nn.Dropout(0.5),
            #        *bn_relu_conv(c_out, c_out, 3)
            #)
            #self.c11 = nn.Sequential(*bn_relu_conv(c_in, c_out, 1))
            self.c33 = nn.Sequential(
                    *conv_relu_bn(c_in, c_out, 3),
                    nn.Dropout(0.5),
                    *conv_relu_bn(c_out, c_out, 3)
            )
            self.c11 = nn.Sequential(*conv_relu_bn(c_in, c_out, 1))
        else:
            #self.c33 = nn.Sequential(
            #        *bn_relu_conv(c_in, c_out, 3),
            #        *bn_relu_conv(c_out, c_out, 3)
            #)
            #self.c11 = nn.Sequential(*bn_relu_conv(c_in, c_out, 1))
            self.c33 = nn.Sequential(
                    *conv_relu_bn(c_in, c_out, 3),
                    *conv_relu_bn(c_out, c_out, 3)
            )
            self.c11 = nn.Sequential(*conv_relu_bn(c_in, c_out, 1))


    def forward(self, inputs):
        return self.c33(inputs) + self.c11(inputs)

class WRN(nn.Module):

    def __init__(self, input_dim, num_classes, k, use_dropout):
        super(WRN, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(input_dim[0], 16*k, kernel_size=3, stride=1, padding=1, bias=True),
            WRN_Block(16*k, 16*k, use_dropout), #conv2
            nn.MaxPool2d(kernel_size=2),
            WRN_Block(16*k, 32*k, use_dropout), #conv3
            nn.MaxPool2d(kernel_size=2),
            WRN_Block(32*k, 64*k, use_dropout), #conv4
            nn.AdaptiveAvgPool2d((1,1))
        )

        probe_tensor = torch.zeros((1,) + input_dim)
        features = self.features(probe_tensor)
        print("Feature maps size : {}".format(features.shape))
        features_dim = features.view(-1)

        self.classifier = nn.Linear(features_dim.shape[0], num_classes)

    def penalty(self):
        penalty_term = torch.zeros([])
        penalty_term += self.classifier.weight.norm(2)
        #print("Modules :")
        #print(list(self.modules()))
        #for m in self.modules():
        #    if type(m) in [nn.Conv2d, nn.Linear]:
        #        print("**** {}".format(type(m)))
        #    else:
        #        print("{}".format(type(m)))
        #import sys
        #sys.exit(-1)
        return penalty_term

    def forward(self, inputs):
        features = self.features(inputs)
        features = features.view(features.size()[0], -1)
        return self.classifier(features)


model_builder = {'linear': Linear,
                 'cnn': lambda idim, nc, dropout: CNN(idim, nc, dropout),
                 'wrn': lambda idim, nc, dropout: WRN(idim, nc, 5, dropout)}


def build_model(model_name  : str,
                input_dim   : tuple,
                num_classes : int,
                use_dropout : bool):
    return model_builder[model_name](input_dim, num_classes, use_dropout)


if __name__ == '__main__':

    input_dim   = (3, 32, 32)
    num_classes = 100
    model_name  = 'cnn'
    batch_size  = 4

    model = build_model(model_name, input_dim, num_classes)

    inputs = torch.randn((batch_size,) + input_dim)
    outputs = model(inputs)

    print(outputs.shape)
