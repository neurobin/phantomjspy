# -*- coding: utf-8 -*-

import json
import logging
import os
import re
import subprocess as sbp


class Keys(object):
    url = 'url'
    proxy = 'proxy'
    proxy_type = 'proxy_type'
    selector = 'selector'
    max_wait = 'max_wait'
    min_wait = 'min_wait'
    js_path = 'js_path'
    ssl_verify = 'ssl_verify'
    load_images = 'load_images'


class Phantom(object):

    def __init__(self, logger=None, exec_path='phantomjs', process_timeout=120):
        self.process_timeout = process_timeout
        self.exec_path = exec_path
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger(__name__)

    def syscall(self, cmd):
        """cmd is a list comprising the command and the arguments
        """
        try:
            proc = sbp.Popen(cmd, stdout=sbp.PIPE, stderr=sbp.PIPE)
            output, errors = proc.communicate(timeout=self.process_timeout)
            # return sbp.check_output(cmd)
            self.logger.error(errors)
            if output:
                # return output.decode('utf-8')
                res = output.decode('utf-8')
                if res.startswith('E: Phantomjs failed to open page'):
                    self.logger.error(res)
                    res = ''
                return res
            # import sys
            # print(sys.stdout.encoding)
            # proc = sbp.run(cmd, stdout=sbp.PIPE, encoding='utf-8', timeout=self.process_timeout)
            # return proc.stdout
        except sbp.CalledProcessError:
            self.logger.exception("E: PhantomJS command failed")
        except:
            self.logger.exception("E: Unknown PhantomJS error")
        return ''

    def download_page(self, conf, proxy='', proxy_type='', js_path='', ssl_verify=True,
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

        output = self.syscall(cmd)
        # output = self.syscall(['phantomjs', '-h',])
        # self.logger.debug(output)
        return output

    @staticmethod
    def get_bounded_data(output):
        output = re.sub(r'[\s\S]*###DATA_START###', '', output, flags=re.M)
        output = re.sub(r'###DATA_END###[\s\S]*', '', output, flags=re.M)
        return output.strip()
