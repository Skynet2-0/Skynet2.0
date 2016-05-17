from Tribler.Core.SessionConfig import SessionStartupConfig
from Tribler.Core.Session import Session

class ExitNode(object):
	'''
	Modification of the tunnel main.py
	Used to run an exitnode instance with multichain enabled
	'''

	__single = None	
	
	def __init__(self):
		'''
		initializes a tribler exit node on the system
		ToDo: maybe the class should be singleton?
		'''
		if ExitNode.__single:
			raise RuntimeError("ExitNode is singleton")
		ExitNode.__single = self
		self.start()
		
	def get_instance(*args, **kw):
		if ExitNode.__single is None:
			ExitNodel(*args, **kw)
		return ExitNode.__single
	get_instance = staticmethod(get_instance)
		
	def start(self):
		'''
		Start a tribler session, with some user experience functions turned off.
		with multichain and being an exitnode explicitly turned on
		'''
		config = SessionStartupConfig()
		config.set_enable_multichain(True)		
		config.set_tunnel_community_exitnode_enabled(True)

		config.set_videoplayer(False)
      
		self.session = Session(config)
 		
 		#session is now initialized
      
		upgrader = self.session.prestart()
		while not upgrader.is_done:
			time.sleep(0.1)
		self.session.prestart()
		#logger.info("Using port %d" % self.session.get_dispersy_port())
      
		self.session.start()