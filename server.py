#!/usr/bin/env python
# https://github.com/teknogods/eaEmu/blob/master/eaEmu/gamespy/webServices.py

import sys
import logging
import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    # generate the classes with 'wsdl2py -wb http://redalert3pc.sake.gamespy.com/SakeStorageServer/StorageServer.asmx?WSDL'
    from soap.StorageServer_server import *
    from soap.AuthService_server import *
    from soap.CompetitionService_server import *

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.web.resource import NoResource
from twisted.internet import reactor, endpoints
from twisted.python import log

class BlankPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        return 'No message of the day'

class AuthServiceImpl(AuthService):

    def soap_LoginUniqueNick(self, ps, **kw):
        #try:
        log.msg('soap_LoginUniqueNick')
        #request = ps.Parse(LoginUniqueNickSoapIn.typecode)
        #LOG.debug(request.__dict__)
        result = LoginUniqueNickSoapOut()
        result.LoginUniqueNickResult = result.new_LoginUniqueNickResult()
        result.LoginUniqueNickResult.ResponseCode = 0
        result.LoginUniqueNickResult.Certificate = result.LoginUniqueNickResult.new_certificate()
        result.LoginUniqueNickResult.Certificate.Length = 303
        result.LoginUniqueNickResult.Certificate.Version = 1
        result.LoginUniqueNickResult.Certificate.Partnercode = 11067
        result.LoginUniqueNickResult.Certificate.Namespaceid = 2
        result.LoginUniqueNickResult.Certificate.Userid =  11111
        result.LoginUniqueNickResult.Certificate.Profileid = 22222
        result.LoginUniqueNickResult.Certificate.Expiretime = 0
        result.LoginUniqueNickResult.Certificate.Profilenick = 'Jackalus'
        result.LoginUniqueNickResult.Certificate.Uniquenick = 'Jackalus'
        result.LoginUniqueNickResult.Certificate.Cdkeyhash = '1234'
        result.LoginUniqueNickResult.Certificate.Peerkeymodulus = '95375465E3FAC4900FC912E7B30EF7171B0546DF4D185DB04F21C79153CE091859DF2EBDDFE5047D80C2EF86A2169B05A933AE2EAB2962F7B32CFE3CB0C25E7E3A26BB6534C9CF19640F1143735BD0CEAA7AA88CD64ACEC6EEB037007567F1EC51D00C1D2F1FFCFECB5300C93D6D6A50C1E3BDF495FC17601794E5655C476819' #256 chars
        result.LoginUniqueNickResult.Certificate.Peerkeyexponent = '010001'
        result.LoginUniqueNickResult.Certificate.Serverdata = '908EA21B9109C45591A1A011BF84A18940D22E032601A1B2DD235E278A9EF131404E6B07F7E2BE8BF4A658E2CB2DDE27E09354B7127C8A05D10BB4298837F96518CCB412497BE01ABA8969F9F46D23EBDE7CC9BE6268F0E6ED8209AD79727BC8E0274F6725A67CAB91AC87022E5871040BF856E541A76BB57C07F4B9BE4C6316' #256 chars
        result.LoginUniqueNickResult.Certificate.Signature = '181A4E679AC27D83543CECB8E1398243113EF6322D630923C6CD26860F265FC031C2C61D4F9D86046C07BBBF9CF86894903BD867E3CB59A0D9EFDADCB34A7FB3CC8BC7650B48E8913D327C38BB31E0EEB06E1FC1ACA2CFC52569BE8C48840627783D7FFC4A506B1D23A1C4AEAF12724DEB12B5036E0189E48A0FCB2832E1FB00'.decode('hex') #256 chars
        result.LoginUniqueNickResult.Certificate.Timestamp = 'U3VuZGF5LCBPY3RvYmVyIDE4LCAyMDA5IDE6MTk6NTMgQU0='

        result.LoginUniqueNickResult.Peerkeyprivate = '8818DA2AC0E0956E0C67CA8D785CFAF3A11A9404D1ED9A6E580EA8569E087B75316B85D77B2208916BE2E0D37C7D7FD18EFD6B2E77C11CDA6E1B689BF460A40BBAF861D800497822004880024B4E7F98A020B1896F536D7219E67AB24B17D60A7BDD7D42E3501BB2FA50BB071EF7A80F29870FFD7C409C0B7BB7A8F70489D04D'.decode('hex')
        return None, result
        #except Exception as ex:
        #    LOG.exception('soap_LoginUniqueNick failed')

class FieldValue(object):
    allowed_types = set((
        'ByteValue',
        'ShortValue',
        'IntValue',
        'FloatValue',
        'AsciiStringValue',
        'UnicodeStringValue',
        'BooleanValue',
        'DateAndTimeValue',
        'BinaryDataValue',
        'Int64Value',
    ))

    def __init__(self, initial_type='AsciiStringValue', value=''):
        self.type = initial_type
        self.value = value

    def __str__(self):
        return '<(%s) %s>' % (self.type, self.value)

    def __repr__(self):
        return 'FieldValue(%s, %s)' % (repr(self.type), repr(self.value))

    @staticmethod
    def from_soap_record(obj):
        """Takes a RecordValue"""
        if obj.ByteValue != None:
            return FieldValue('ByteValue', int(obj.ByteValue.Value))
        elif obj.ShortValue != None:
            return FieldValue('ShortValue', int(obj.ShortValue.Value))
        elif obj.IntValue != None:
            return FieldValue('IntValue', int(obj.IntValue.Value))
        elif obj.FloatValue != None:
            return FieldValue('FloatValue', float(obj.FloatValue.Value))
        elif obj.AsciiStringValue != None:
            return FieldValue('AsciiStringValue', obj.AsciiStringValue.Value)
        elif obj.UnicodeStringValue != None:
            return FieldValue('UnicodeStringValue', obj.UnicodeStringValue.Value)
        elif obj.BooleanValue != None:
            return FieldValue('BooleanValue', obj.BooleanValue.Value)
        elif obj.DateAndTimeValue != None:
            return FieldValue('DateAndTimeValue', obj.DateAndTimeValue.Value)
        elif obj.BinaryDataValue != None:
            return FieldValue('BinaryDataValue', obj.BinaryDataValue.Value)
        elif obj.Int64Value != None:
            return FieldValue('Int64Value', obj.Int64Value.Value)
        return None

    def to_soap_record(self, obj):
        """Takes a RecordValue"""
        if self.type == 'ByteValue':
            obj.ByteValue = obj.new_byteValue()
            obj.ByteValue.Value = self.value
        elif self.type == 'ShortValue':
            obj.ShortValue = obj.new_shortValue()
            obj.ShortValue.Value = self.value
        elif self.type == 'IntValue':
            obj.IntValue = obj.new_intValue()
            obj.IntValue.Value = self.value
        elif self.type == 'FloatValue':
            obj.FloatValue = obj.new_floatValue()
            obj.FloatValue.Value = self.value
        elif self.type == 'AsciiStringValue':
            obj.AsciiStringValue = obj.new_asciiStringValue()
            obj.AsciiStringValue.Value = self.value
        elif self.type == 'UnicodeStringValue':
            obj.UnicodeStringValue = obj.new_unicodeStringValue()
            obj.UnicodeStringValue.Value = self.value
        elif self.type == 'BooleanValue':
            obj.BooleanValue = obj.new_booleanValue()
            obj.BooleanValue.Value = self.value
        elif self.type == 'DateAndTimeValue':
            obj.DateAndTimeValue = obj.new_dateAndTimeValue()
            obj.DateAndTimeValue.Value = self.value
        elif self.type == 'BinaryDataValue':
            obj.BinaryDataValue = obj.new_binaryDataValue()
            obj.BinaryDataValue.Value = self.value
        elif self.type == 'Int64Value':
            obj.Int64Value = obj.new_int64Value()
            obj.Int64Value.Value = self.value

storage_tables = {
    'PersonalInfo': [
        {
            'ownerid': FieldValue('IntValue', 100000001),
            'recordid': FieldValue('IntValue', 0),
            'ViewMyProfile': FieldValue('IntValue', 0),
            'EmailAddress': FieldValue('AsciiStringValue', '<not available here yet>'),
            'ViewMyEmail': FieldValue('IntValue', 0),
            'AccountCreationDate': FieldValue('DateAndTimeValue', (2018, 1, 1, 0, 0, 0, 0, 0, 0)),
            'LastGameDate': FieldValue('DateAndTimeValue', (2018, 1, 1, 0, 0, 0, 0, 0, 0)),
            'CampaignsCompleted': FieldValue('ByteValue', 0),
            'NickName': FieldValue('AsciiStringValue', 'mynick'),
        }
    ],

    'PlayerStats_v1': [
    ]
}

class StorageServerImpl(StorageServer):

    def soap_SearchForRecords(self, ps, **kw):
        try:
            request = ps.Parse(SearchForRecordsSoapIn.typecode)
            log.msg('[[**]] SearchForRecords table: %s' % request.Tableid)
            log.msg('[[**]] filter: %s' % str(request.Filter))
            log.msg('[[**]] targetfilter: %s' % str(request.Targetfilter))
            result = SearchForRecordsSoapOut()
            result.SearchForRecordsResult = result.new_SearchForRecordsResult('Success')
            result.Values = result.new_values()
            result.Values.ArrayOfRecordValue = []

            log.msg('[[**]] fields: %s' % ', '.join(request.Fields.String))
    
            table = storage_tables.get(request.Tableid, [])

            # TODO This is where we would do the search. for now return the first record
            resulting_records = table[0:request.Max]

            for record in resulting_records:
                record_value = result.Values.new_ArrayOfRecordValue()

                # Construct a field object to return
                field_values = []
                for field in request.Fields.String:
                    field_value = record_value.new_RecordValue()
                    if field in record:
                        record[field].to_soap_record(field_value)
                    
                    field_values.append(field_value)

                record_value.RecordValue = field_values
                result.Values.ArrayOfRecordValue.append(record_value)

            return request, result
        except Exception as ex:
            logging.exception('[[**]] soap_SearchForRecords failed')

    def soap_CreateRecord(self, ps, **kw):
        try:
            request = ps.Parse(CreateRecordSoapIn.typecode)
            log.msg('[[**]] CreateRecord table: %s' % request.Tableid)

            if request.Tableid not in storage_tables:
                storage_tables[request.Tableid] = []
            table = storage_tables[request.Tableid]

            new_record = {}
            for field in request.Values.RecordField:
                value = FieldValue.from_soap_record(field.Value)
                new_record[field.Name] = value
                log.msg('[[**]] - field: %s = %s' % (field.Name, str(value)))

            record_id = len(table)
            table.append(new_record)

            result = CreateRecordSoapOut()
            result.CreateRecordResult = result.new_CreateRecordResult('Success')
            result.Recordid = record_id
            return request, result
        except Exception as ex:
            logging.exception('[[**]] soap_CreateRecord failed')

    def soap_UpdateRecord(self, ps, **kw):
        try:
            request = ps.Parse(UpdateRecordSoapIn.typecode)
            log.msg('[[**]] UpdateRecord table: %s' % request.Tableid)

            # Pick the record to update
            table = storage_tables.get(request.Tableid, [])
            if request.Recordid >= 0:
                update_record = table[request.Recordid]
            elif len(table) > 0:
                update_record = table[0]
            else:
                update_record = {}

            for field in request.Values.RecordField:
                value = FieldValue.from_soap_record(field.Value)
                update_record[field.Name] = value
                log.msg('[[**]] - field: %s = %s' % (field.Name, str(value)))

            result = UpdateRecordSoapOut()
            result.UpdateRecordResult = result.new_UpdateRecordResult('Success')
            return request, result
        except Exception as ex:
            logging.exception('[[**]] soap_UpdateRecord failed')

class CompetitionServiceImpl(CompetitionService):

    pass

class WebServer(Site):
    def __init__(self):
        root = Resource()

        authService = Resource()
        authService.putChild('AuthService.asmx', AuthServiceImpl())
        root.putChild('AuthService', authService)

        storageService = Resource()
        storageService.putChild('StorageServer.asmx', StorageServerImpl())
        root.putChild('SakeStorageServer', storageService)

        competitionService = Resource()
        competitionService.putChild('CompetitionService.asmx', CompetitionServiceImpl())
        root.putChild('CompetitionService', competitionService)

        motd_service = Resource()
        motd_service.putChild('motd.asp', BlankPage())
        root.putChild('motd', motd_service)

        Site.__init__(self, root)

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
    log.startLogging(sys.stdout)

    listen_port = 80
    if len(sys.argv) > 1:
        listen_port = int(sys.argv[1])
    
    factory = WebServer()
    endpoint = endpoints.TCP4ServerEndpoint(reactor, listen_port)
    endpoint.listen(factory)
    reactor.run()
