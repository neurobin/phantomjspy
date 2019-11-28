# -*- coding: utf-8 -*-

import os
import subprocess as sbp
import re
import logging


class Phantom(object):

    def __init__(self, logger=None, exec_path='phantomjs', process_timeout=120):
        self.process_timeout = process_timeout
        self.exec_path = exec_path
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger(self.__class__)

    def syscall(self, cmd):
        """cmd is a list comprising the command and the arguments
        """
        try:
            proc = sbp.Popen(cmd, stdout=sbp.PIPE, stderr=sbp.PIPE)
            output, errors = proc.communicate(timeout=self.process_timeout)
            # return sbp.check_output(cmd)
            self.logger.error(errors)
            return output
        except sbp.CalledProcessError as e:
            self.logger.exception("E: PhantomJS command failed")
        return ''

    def download_page(self, url, proxy='', proxy_type='', selector='', timeout='30000', js_path=None, ssl_verify=True):
        cmd = [self.exec_path, '--load-images=false', ]
        if not ssl_verify:
            cmd.append('--ignore-ssl-errors=true')

        if proxy_type:
            cmd.append("--proxy-type=%s" % (proxy_type,))
        if proxy:
            cmd.append("--proxy=%s" % (proxy,))
            
        if not js_path:
            if selector:
                cmd.extend([os.path.join(os.path.dirname(__file__),
                                         'get_source_wait_for.js'), url, selector, timeout])
            else:
                cmd.extend(
                    [os.path.join(os.path.dirname(__file__), 'get_source.js'), url])
        else:
            cmd.extend([js_path, url])
        self.logger.info(cmd)
        output = self.syscall(cmd)
        # output = self.syscall(['phantomjs', '-h',])
        # self.logger.info(output)
        return output
    
    @staticmethod
    def get_bounded_data(output):
        output = re.sub(r'[\s\S]*###DATA_START###', '', output, flags=re.M)
        output = re.sub(r'###DATA_END###[\s\S]*', '', output, flags=re.M)
        return output.strip()
