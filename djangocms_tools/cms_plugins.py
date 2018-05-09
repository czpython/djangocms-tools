from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


class CMSToolsNode(CMSPluginBase):
    render_template = 'djangocms_tools/cmstoolsnode.html'


plugin_pool.register_plugin(CMSToolsNode)
