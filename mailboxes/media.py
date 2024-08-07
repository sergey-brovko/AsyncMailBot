from aiogram.types import InputMediaDocument, InputMediaPhoto, InputMediaAudio, InputMediaVideo, BufferedInputFile


def detect_file_type(filename: str) -> str:
    if filename.split('.')[1] in ('aif', 'aiff', 'wav', 'mid', 'ogg', 'flac', 'mp3',
                                  'aac', 'm4a', 'aifc', 'rm', 'ra', 'wma'):
        return 'Audio'
    if filename.split('.')[1] in ('sxi', 'odg', 'svg', 'vsd', 'eps', 'cwk', 'wp', 'ott', 'asp', 'cdd',
                                  'cpp', 'dotm', 'gpx', 'indd', 'kdc', '.kml', 'mdb', 'mdf', 'mso', 'one',
                                  'pkg', 'pl', 'pot', 'potm', 'potx', 'ppsm', 'ps', 'sdf', 'sgml', 'sldm',
                                  'xar', 'xlt', 'xltm', 'xltx', 'pdf', 'txt', 'doc', 'odt', 'xps', 'chm',
                                  'rtf', 'sxw', 'docx', 'wpd', 'wps', 'docm', "hwp", 'pub', 'xml', 'log',
                                  'oxps', 'vnt', 'dot', 'pages', 'm3u', 'dotx', 'shs', 'msg', 'odm', 'pmd',
                                  'vmg', 'eml', 'tex', 'wp5', 'csk', 'fdxt', 'adoc', 'afpub', 'tcr', 'acsm',
                                  'opf', 'mbp', 'apnx', 'cbt', 'vbk', 'kfx', 'lrf', 'snb', 'odp', 'ppt',
                                  'pptx', 'pps', 'ppsx', 'pptm', 'key', "flipchart", 'epub', 'mobi', 'azw',
                                  'azw3', 'fb2', 'djvu', 'cbz', 'cbr', 'ibooks', 'lit', 'pdb', 'prc', 'tr2',
                                  'tr3', 'ods', 'xls', 'xlsx', 'csv', 'wks', 'xlsm', 'xlsb', 'xlr', 'wk3',
                                  'numbers'):
        return 'Document'
    if filename.split('.')[1] in ('jpg', 'jpeg', 'png', 'gif', 'raw', 'svg', 'bmp', 'ico', 'tiff', 'webp'):
        return 'Photo'
    if filename.split('.', )[1] in ('3g2', '3gp', '3gp2', '3gpp', '3gpp2', 'asf', 'asx', 'avi', 'bin', 'dat', 'drv',
                                    'f4v', 'flv', 'gtp', 'h264', 'm4v', 'mkv', 'mod', 'moov', 'mov', 'mp4', 'mpeg',
                                    'mpg', 'mts', 'rm', 'rmvb', 'spl', 'srt', 'stl', 'swf', 'ts', 'vcd', 'vid', 'vid',
                                    'vid', 'vob', 'webm', 'wm', 'wmv', 'yuv'):
        return 'Video'


def files_to_media(file_tuple: tuple[str, bytes]) -> (InputMediaAudio | InputMediaDocument |
                                                      InputMediaPhoto | InputMediaVideo):
    name, file = file_tuple
    if detect_file_type(name) == 'Document':
        return InputMediaDocument(media=BufferedInputFile(file=file, filename=name))
    if detect_file_type(name) == 'Audio':
        return InputMediaAudio(media=BufferedInputFile(file=file, filename=name))
    if detect_file_type(name) == 'Photo':
        return InputMediaPhoto(media=BufferedInputFile(file=file, filename=name))
    if detect_file_type(name) == 'Video':
        return InputMediaVideo(media=BufferedInputFile(file=file, filename=name))
