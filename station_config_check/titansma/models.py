# This file contains mappings of parameters and values from the
# TitanSMA/centaur configuration file

# This dictionary maps the configuration entries from a TitanSMA config file
# to their respective names
TITANSMA_CONFIG = {
    "<sensor/accelerometer/mode>": "Accelerometer Mode",
    "<retrieval/networkName>": "Network Code",
    "<retrieval/stationName>": 'Station Code',
    "<retrieval/locationName>": "Location Code",
    "<retrieval/channelName#_1>": "Primary Channel 1",
    "<retrieval/channelName#_2>": "Primary Channel 2",
    "<retrieval/channelName#_3>": "Primary Channel 3",
    "<retrieval/channelName#_101>": "Secondary Channel 1",
    "<retrieval/channelName#_102>": "Secondary Channel 2",
    "<retrieval/channelName#_103>": "Secondary Channel 3",
    "<retrieval/sohCode>": "SOH Code",
    "<discovery/enableDiscovery>": "Discovery Enabled",
    "<networking/gateway>": "Gateway IP",
    "<networking/mode>": "IP Mode",
    "<networking/netmask>": "Network Mask",
    "<networking/staticDns/primary>": "Primary DNS",
    "<networking/staticDns/secondary>": "Secondary DNS",
    "<networking/staticip>": "Static IP",
    "<dataArchive/enable>": "Data Archiving",
    "<dataArchive/enable/soh>": "Archiving SOH",
    "<dataArchive/filtered/scnlList>": "Archive SNCL",
    "<apollo/consistentLatency>": "Consistent Latency",
    "<system/fieldNaming>": "Field Naming",
    "<system/onlyUseNp2Packets>": "Libra Compatibility Mode",
    "<digitizer/sampleRate>": "Primary Channels Sample Rate",
    "<digitizer/framesPerPacket>": "Primary Channels Frames per Packet",
    "<digitizer/channels/outputType>": "Primary Channels Output Type",
    "<digitizer/sampleEncoding>": "Primary Channels Sample Encoding",
    "<digitizer/sampleRate#_101>": "Secondary Channels Sample Rate",
    "<digitizer/framesPerPacket#_101>": "Secondary Channels Frames per Packet",
    "<digitizer/channels/outputType_#101>": "Secondary Channels Output Type",
    "<digitizer/sampleEncoding#_101>": "Secondary Channels Sample Encoding",
    "<sohReportInterval>": "SOH Report Interval",
    "<seedlinkServerLibrary/table/_exists#_1>": "Seedlink Server Exists",
    "<timing/source>": "Timing Source",
    "<ntp/serverAddress>": "NTP Server Address",
    "<timing/server>": "Time Sharing",
    "<setTimeUsingNtpOnStartup>": "Set Time With NTP at Startup"
}

NP_CONFIG = {
    "<streamingData/name#_{i}>": "Name",
    "<streamingData/enable#_{i}>": "Enabled",
    "<streamingData/ipAddress#_{i}>": "IP Address",
    "<streamingData/portNumber#_{i}>": "Port Number",
    "<streamingData/timeSeriesEnable#_{i}>": "Streaming Primary Time Series",
    "<streamingData/subsampledTimeSeriesEnable#_{i}>":
    "Streaming Secondary Time Series",
    "<streamingData/enable/alerts#_{i}>": "Streaming Alerts",
    "<streamingData/enable/raw#_{i}>": "Streaming Raw Data",
    "<streamingData/enable/soh/arm#_{i}>": "Streaming ARM SOH",
    "<streamingData/enable/soh/system#_{i}>": "Streaming System SOH",
    "<streamingData/enable/triggers#_{i}>": "Streaming Triggers",
    "<streamingData/multicastTimeToLive#_{i}>": "Multicast TTL",
    "<streamingData/retxStrategy#_{i}>": "ReTX Strategy",
    "<streamingData/shortTermCompleteThreshold#_{i}>":
    "Short Term Complete Threshold",
    "<streamingData/throttle/enable#_{i}>": "Throttle",
    "<streamingData/throttle/maxBitRate#_{i}>": "Throttle Bitrate"
}

WEBSOCKET_CONFIG = {
    "<streamingDataLibrary/table/filtered/websocket/_exists#_{i}>":
    "Websocket Streamer {i}",
    "<streamingData/name/websocket#_{i}>": "Name",
    "<streamingData/enable/websocket#_{i}>": "Enabled",
    "<streamingData/ipAddress/websocket#_{i}>": "IP Address",
    "<streamingData/portNumber/websocket#_{i}>": "Port Number",
    "<streamingData/enable/tls/websocket#_{i}>": "TLS Enabled",
    "<streamingData/timeSeriesEnable/websocket#_{i}>":
    "Streaming Primary Time Series",
    "<streamingData/subsampledTimeSeriesEnable/websocket#_{i}>":
    "Streaming Secondary Time Series",
    "<streamingData/enable/alerts/websocket#_{i}>": "Streaming Alerts",
    "<streamingData/enable/raw/websocket#_{i}>": "Streaming Raw Data",
    "<streamingData/enable/soh/arm/websocket#_{i}>": "Streaming ARM SOH",
    "<streamingData/enable/soh/system/websocket#_{i}>": "Streaming System SOH",
    "<streamingData/enable/triggers/websocket#_{i}>": "Streaming Triggers",
    "<streamingData/multicastTimeToLive/websocket#_{i}>": "Multicast TTL",
    "<streamingData/retxStrategy/websocket#_{i}>": "ReTX Strategy",
    "<streamingData/shortTermCompleteThreshold/websocket#_{i}>":
    "Short Term Complete Threshold",
    "<streamingData/throttle/enable/websocket#_{i}>": "Throttle",
    "<streamingData/throttle/maxBitRate/websocket#_{i}>": "Throttle Bitrate"
}
