# encoding: utf-8

'''plugin.py

'''
import ckan.lib.uploader as uploader
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from location import geores
import os
import logging

log = logging.getLogger(__name__)

class LocationPlugin(plugins.SingletonPlugin, DefaultTranslation):
    '''
    An example theme plugin.
    '''
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IUploader)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')

        # Register this plugin's fanstatic directory with CKAN.
        # Here, 'fanstatic' is the path to the fanstatic directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this fanstatic directory from CKAN
        # templates.
        toolkit.add_resource('fanstatic', 'location')

    def get_resource_uploader(self, data_dict):
        return MyResourceUploader(data_dict)

    def get_uploader(self, upload_to, old_filename=None):
        return uploader.Upload(upload_to, old_filename)


class MyResourceUploader(uploader.ResourceUpload):
    def __init__(self, data_dict):
        super(MyResourceUploader, self).__init__(data_dict)
        self.data_dict = data_dict

    def get_directory(self, id):
        return super(MyResourceUploader, self).get_directory(id)

    def get_path(self, id):
        return super(MyResourceUploader, self).get_path(id)

    def upload(self, id, max_size=10):
        '''Actually upload the file.

        :returns: ``'file uploaded'`` if a new file was successfully uploaded
            (whether it overwrote a previously uploaded file or not),
            ``'file deleted'`` if an existing uploaded file was deleted,
            or ``None`` if nothing changed
        :rtype: ``string`` or ``None``

        '''
        if not self.storage_path:
            return

        # Get directory and filepath on the system
        # where the file for this resource will be stored
        directory = self.get_directory(id)
        filepath = self.get_path(id)

        # If a filename has been provided (a file is being uploaded)
        # we write it to the filepath (and overwrite it if it already
        # exists). This way the uploaded file will always be stored
        # in the same location
        if self.filename:
            try:
                os.makedirs(directory)
            except OSError, e:
                # errno 17 is file already exists
                if e.errno != 17:
                    raise
            tmp_filepath = filepath + '~'
            output_file = open(tmp_filepath, 'wb+')
            self.upload_file.seek(0)
            current_size = 0
            while True:
                current_size = current_size + 1
                # MB chunks
                data = self.upload_file.read(2 ** 20)

                if not data:
                    break
                output_file.write(data)
                if current_size > max_size:
                    os.remove(tmp_filepath)
                    raise toolkit.ValidationError(
                        {'upload': ['File upload too large']}
                    )

            output_file.close()

            geores(tmp_filepath, self.data_dict)
            os.rename(tmp_filepath, filepath)
            return

        # The resource form only sets self.clear (via the input clear_upload)
        # to True when an uploaded file is not replaced by another uploaded
        # file, only if it is replaced by a link to file.
        # If the uploaded file is replaced by a link, we should remove the
        # previously uploaded file to clean up the file system.
        if self.clear:
            try:
                os.remove(filepath)
            except OSError, e:
                pass
