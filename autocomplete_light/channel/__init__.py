from .base import ChannelBase
from .json import JSONChannelBase
from .remote import RemoteChannelBase
from .generic import GenericModelChannelBackendMixin
from .template import TemplateChannelFrontendMixin
from .model import ModelChannelBackendMixin

class ModelTemplateChannel(TemplateChannelFrontendMixin, ModelChannelBackendMixin, ChannelBase):
    pass

class GenericTemplateChannel(TemplateChannelFrontendMixin, GenericModelChannelBackendMixin, ChannelBase):
    pass
