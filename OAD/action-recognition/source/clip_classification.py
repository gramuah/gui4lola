import torch
from c3d_model import C3D


class C3DClipClassification():

    def __init__(self, clip_length=16):

        # C3D parameters
        self.clip_length = clip_length
        self.model_path = './OAD/action-recognition/models/C3D_UCF101_bs20_epochs50_lr0.0001/model/' \
                          'params.pkl'

        # Prepare for GPU
        use_cuda = torch.cuda.is_available()
        self.device = torch.device('cuda:0' if use_cuda else 'cpu')

        # Load C3D model
        self.c3d = C3D(num_classes=101, pretrained=False)
        self.c3d.load_state_dict(torch.load(self.model_path))
        self.c3d.to(self.device)
        self.c3d.eval()

        return

    def clip_classification(self, clip):

        clip = torch.from_numpy(clip)
        clip = clip.to(self.device)
        outputs = self.c3d(clip)
        prob = torch.nn.Softmax(dim=1)(outputs)
        pred = torch.max(prob, 1)[1].detach().cpu().numpy()[0]

        return prob, pred
