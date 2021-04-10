
import logging
import json
import os
import re
import asyncio
from typing import List, Dict, Any

class Phantom(object):

    def __init__(self, logger=None, exec_path='phantomjs', process_timeout=120):
        self.process_timeout = process_timeout
        self.exec_path = exec_path
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger(self.__class__.__name__)

    async def syscall(self, cmd: List[str]):
        """cmd is a list comprising the command and the arguments
        """
        try:
            proc = await asyncio.create_subprocess_exec(*cmd,
                                                        stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE)
            # output, errors = await proc.communicate(timeout=self.process_timeout)
            # task = asyncio.Task(proc.communicate())
            output, errors = await asyncio.wait_for(proc.communicate(), self.process_timeout)
            # errors = await proc.stderr.read()
            self.logger.error(errors)
            # output = await proc.stdout.read()
            if output:
                res: str = output.decode('utf-8')
                if res.startswith('E: Phantomjs failed to open page'):
                    self.logger.error(res)
                    res = ''
                return res
        except:
            self.logger.exception("E: PhantomJS command failed")
        return ''

    async def download_page(self, conf, proxy='', proxy_type='', js_path='', ssl_verify=True,
                      load_images=False, cookies_file=''):
        confs = json.dumps(conf)

        cmd = [self.exec_path]

        if not load_images:
            cmd.append('--load-images=false')

        if not ssl_verify:
            cmd.append('--ignore-ssl-errors=true')

        if proxy_type:
            cmd.append("--proxy-type=%s" % (proxy_type,))
        if proxy:
            cmd.append("--proxy=%s" % (proxy,))
        if cookies_file:
            cmd.append("--cookies-file=%s" % (cookies_file,))

        if not js_path:
            cmd.extend([os.path.join(os.path.dirname(__file__), 'get_source_wait_for.js'), confs])
        else:
            cmd.extend([js_path, confs])

        self.logger.debug(cmd)

        output = await self.syscall(cmd)
        return output

    @staticmethod
    def get_bounded_data(output):
        output = re.sub(r'[\s\S]*###DATA_START###', '', output, flags=re.M)
        output = re.sub(r'###DATA_END###[\s\S]*', '', output, flags=re.M)
        return output.strip()
