# Project imports
from imp import load_source
import os
import sys
import shutil

from click.testing import CliRunner
from nose.plugins.skip import SkipTest
from nose.tools import assert_raises
from six import text_type, unichr as six_unichr

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))))

import helper
elodie = load_source('elodie', os.path.abspath('{}/../../elodie.py'.format(os.path.dirname(os.path.realpath(__file__)))))

from elodie import constants
from elodie.localstorage import Db
from elodie.media.audio import Audio
from elodie.media.photo import Photo
from elodie.media.text import Text
from elodie.media.video import Video

os.environ['TZ'] = 'GMT'

def test_import_file_text():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    dest_path = elodie.import_file(origin, folder_destination, False, False, False)
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert helper.path_tz_fix(os.path.join('2016-04-Apr','Unknown Location','2016-04-07_11-15-26-valid-sample-title.txt')) in dest_path, dest_path

def test_import_file_audio():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/audio.m4a' % folder
    shutil.copyfile(helper.get_file('audio.m4a'), origin)

    reset_hash_db()
    dest_path = elodie.import_file(origin, folder_destination, False, False, False)
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert helper.path_tz_fix(os.path.join('2016-01-Jan','Houston','2016-01-04_05-28-15-audio.m4a')) in dest_path, dest_path

def test_import_file_photo():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/plain.jpg' % folder
    shutil.copyfile(helper.get_file('plain.jpg'), origin)

    reset_hash_db()
    dest_path = elodie.import_file(origin, folder_destination, False, False, False)
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert helper.path_tz_fix(os.path.join('2015-12-Dec','Unknown Location','2015-12-05_00-59-26-plain.jpg')) in dest_path, dest_path

def test_import_file_video():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/video.mov' % folder
    shutil.copyfile(helper.get_file('video.mov'), origin)

    reset_hash_db()
    dest_path = elodie.import_file(origin, folder_destination, False, False, False)
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert helper.path_tz_fix(os.path.join('2015-01-Jan','California','2015-01-19_12-45-11-video.mov')) in dest_path, dest_path

def test_import_file_path_unicode():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = text_type(folder)+u'/unicode'+six_unichr(160)+u'filename.txt'
    origin = origin.encode('utf-8')

    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    dest_path = elodie.import_file(origin, folder_destination, False, False, False)
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert helper.path_tz_fix(os.path.join('2016-04-Apr','Unknown Location',u'2016-04-07_11-15-26-unicode\xa0filename-sample-title.txt')) in dest_path, dest_path
    
def test_import_file_allow_duplicate_false():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    dest_path1 = elodie.import_file(origin, folder_destination, False, False, False)
    dest_path2 = elodie.import_file(origin, folder_destination, False, False, False)
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert dest_path1 is not None
    assert dest_path2 is None

def test_import_file_allow_duplicate_true():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    dest_path1 = elodie.import_file(origin, folder_destination, False, False, True)
    dest_path2 = elodie.import_file(origin, folder_destination, False, False, True)
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert dest_path1 is not None
    assert dest_path2 is not None
    assert dest_path1 == dest_path2

def test_import_file_send_to_trash_false():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    dest_path1 = elodie.import_file(origin, folder_destination, False, False, False)
    assert os.path.isfile(origin), origin
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert dest_path1 is not None

def test_import_file_send_to_trash_true():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    dest_path1 = elodie.import_file(origin, folder_destination, False, True, False)
    assert not os.path.isfile(origin), origin
    restore_hash_db()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert dest_path1 is not None

def test_import_destination_in_source():
    temporary_folder, folder = helper.create_working_folder()
    folder_destination = '{}/destination'.format(folder)
    os.mkdir(folder_destination)

    origin = '%s/video.mov' % folder
    shutil.copyfile(helper.get_file('video.mov'), origin)

    reset_hash_db()
    dest_path = elodie.import_file(origin, folder_destination, False, False, False)
    restore_hash_db()

    shutil.rmtree(folder)

    assert dest_path is None, dest_path

def test_update_location_on_audio():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/audio.m4a' % folder
    shutil.copyfile(helper.get_file('audio.m4a'), origin)

    audio = Audio(origin)
    metadata = audio.get_metadata()

    reset_hash_db()
    status = elodie.update_location(audio, origin, 'Sunnyvale, CA')
    restore_hash_db()

    audio_processed = Audio(origin)
    metadata_processed = audio_processed.get_metadata()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert status == True, status
    assert metadata['latitude'] != metadata_processed['latitude'], metadata_processed['latitude']
    assert helper.isclose(metadata_processed['latitude'], 37.36883), metadata_processed['latitude']
    assert helper.isclose(metadata_processed['longitude'], -122.03635), metadata_processed['longitude']

def test_update_location_on_photo():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/plain.jpg' % folder
    shutil.copyfile(helper.get_file('plain.jpg'), origin)

    photo = Photo(origin)
    metadata = photo.get_metadata()

    reset_hash_db()
    status = elodie.update_location(photo, origin, 'Sunnyvale, CA')
    restore_hash_db()

    photo_processed = Photo(origin)
    metadata_processed = photo_processed.get_metadata()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert status == True, status
    assert metadata['latitude'] != metadata_processed['latitude']
    assert helper.isclose(metadata_processed['latitude'], 37.36883), metadata_processed['latitude']
    assert helper.isclose(metadata_processed['longitude'], -122.03635), metadata_processed['longitude']

def test_update_location_on_text():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/text.txt' % folder
    shutil.copyfile(helper.get_file('text.txt'), origin)

    text = Text(origin)
    metadata = text.get_metadata()

    reset_hash_db()
    status = elodie.update_location(text, origin, 'Sunnyvale, CA')
    restore_hash_db()

    text_processed = Text(origin)
    metadata_processed = text_processed.get_metadata()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert status == True, status
    assert metadata['latitude'] != metadata_processed['latitude']
    assert helper.isclose(metadata_processed['latitude'], 37.36883), metadata_processed['latitude']
    assert helper.isclose(metadata_processed['longitude'], -122.03635), metadata_processed['longitude']

def test_update_location_on_video():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/video.mov' % folder
    shutil.copyfile(helper.get_file('video.mov'), origin)

    video = Video(origin)
    metadata = video.get_metadata()

    reset_hash_db()
    status = elodie.update_location(video, origin, 'Sunnyvale, CA')
    restore_hash_db()

    video_processed = Video(origin)
    metadata_processed = video_processed.get_metadata()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert status == True, status
    assert metadata['latitude'] != metadata_processed['latitude']
    assert helper.isclose(metadata_processed['latitude'], 37.36883), metadata_processed['latitude']
    assert helper.isclose(metadata_processed['longitude'], -122.03635), metadata_processed['longitude']

def test_update_time_on_audio():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/audio.m4a' % folder
    shutil.copyfile(helper.get_file('audio.m4a'), origin)

    audio = Audio(origin)
    metadata = audio.get_metadata()

    reset_hash_db()
    status = elodie.update_time(audio, origin, '2000-01-01 12:00:00')
    restore_hash_db()

    audio_processed = Audio(origin)
    metadata_processed = audio_processed.get_metadata()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert status == True, status
    assert metadata['date_taken'] != metadata_processed['date_taken']
    assert metadata_processed['date_taken'] == helper.time_convert((2000, 1, 1, 12, 0, 0, 5, 1, 0)), metadata_processed['date_taken']

def test_update_time_on_photo():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/plain.jpg' % folder
    shutil.copyfile(helper.get_file('plain.jpg'), origin)

    photo = Photo(origin)
    metadata = photo.get_metadata()

    reset_hash_db()
    status = elodie.update_time(photo, origin, '2000-01-01 12:00:00')
    restore_hash_db()

    photo_processed = Photo(origin)
    metadata_processed = photo_processed.get_metadata()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert status == True, status
    assert metadata['date_taken'] != metadata_processed['date_taken']
    assert metadata_processed['date_taken'] == helper.time_convert((2000, 1, 1, 12, 0, 0, 5, 1, 0)), metadata_processed['date_taken']

def test_update_time_on_text():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/text.txt' % folder
    shutil.copyfile(helper.get_file('text.txt'), origin)

    text = Text(origin)
    metadata = text.get_metadata()

    reset_hash_db()
    status = elodie.update_time(text, origin, '2000-01-01 12:00:00')
    restore_hash_db()

    text_processed = Text(origin)
    metadata_processed = text_processed.get_metadata()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert status == True, status
    assert metadata['date_taken'] != metadata_processed['date_taken']
    assert metadata_processed['date_taken'] == helper.time_convert((2000, 1, 1, 12, 0, 0, 5, 1, 0)), metadata_processed['date_taken']

def test_update_time_on_video():
    temporary_folder, folder = helper.create_working_folder()
    temporary_folder_destination, folder_destination = helper.create_working_folder()

    origin = '%s/video.mov' % folder
    shutil.copyfile(helper.get_file('video.mov'), origin)

    video = Video(origin)
    metadata = video.get_metadata()

    reset_hash_db()
    status = elodie.update_time(video, origin, '2000-01-01 12:00:00')
    restore_hash_db()

    video_processed = Video(origin)
    metadata_processed = video_processed.get_metadata()

    shutil.rmtree(folder)
    shutil.rmtree(folder_destination)

    assert status == True, status
    assert metadata['date_taken'] != metadata_processed['date_taken']
    assert metadata_processed['date_taken'] == helper.time_convert((2000, 1, 1, 12, 0, 0, 5, 1, 0)), metadata_processed['date_taken']

def test_regenerate_db_invalid_source():
    runner = CliRunner()
    result = runner.invoke(elodie._generate_db, ['--source', '/invalid/path'])
    assert result.exit_code == 1, result.exit_code

def test_regenerate_valid_source():
    temporary_folder, folder = helper.create_working_folder()

    origin = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    runner = CliRunner()
    result = runner.invoke(elodie._generate_db, ['--source', folder])
    db = Db()
    restore_hash_db()

    shutil.rmtree(folder)

    assert result.exit_code == 0, result.exit_code
    assert 'bde2dc0b839a5d20b0b4c1f57605f84e0e2a4562aaebc1c362de6cb7cc02eeb3' in db.hash_db, db.hash_db

def test_regenerate_valid_source_with_invalid_files():
    temporary_folder, folder = helper.create_working_folder()

    origin_valid = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin_valid)
    origin_invalid = '%s/invalid.invalid' % folder
    shutil.copyfile(helper.get_file('invalid.invalid'), origin_invalid)

    reset_hash_db()
    runner = CliRunner()
    result = runner.invoke(elodie._generate_db, ['--source', folder])
    db = Db()
    restore_hash_db()

    shutil.rmtree(folder)

    assert result.exit_code == 0, result.exit_code
    assert 'bde2dc0b839a5d20b0b4c1f57605f84e0e2a4562aaebc1c362de6cb7cc02eeb3' in db.hash_db, db.hash_db
    assert 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855' not in db.hash_db, db.hash_db

def test_verify_ok():
    temporary_folder, folder = helper.create_working_folder()

    origin = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    runner = CliRunner()
    runner.invoke(elodie._generate_db, ['--source', folder])
    result = runner.invoke(elodie._verify)
    restore_hash_db()

    shutil.rmtree(folder)

    assert 'Success         1' in result.output, result.output
    assert 'Error           0' in result.output, result.output

def test_verify_error():
    temporary_folder, folder = helper.create_working_folder()

    origin = '%s/valid.txt' % folder
    shutil.copyfile(helper.get_file('valid.txt'), origin)

    reset_hash_db()
    runner = CliRunner()
    runner.invoke(elodie._generate_db, ['--source', folder])
    with open(origin, 'w') as f:
        f.write('changed text')
    result = runner.invoke(elodie._verify)
    restore_hash_db()

    shutil.rmtree(folder)

    assert origin in result.output, result.output
    assert 'Error           1' in result.output, result.output

def reset_hash_db():
    hash_db = constants.hash_db
    if os.path.isfile(hash_db):
        os.rename(hash_db, '{}-test'.format(hash_db))

def restore_hash_db():
    hash_db = '{}-test'.format(constants.hash_db)
    if os.path.isfile(hash_db):
        os.rename(hash_db, hash_db.replace('-test', ''))
