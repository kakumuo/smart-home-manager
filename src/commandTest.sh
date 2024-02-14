# configuration:
# queueserver = uspro-opdmq-broker1.aqara.com:9876
# queuetopic = 116919905883855667241b3f
# queueaccesskey = K.1169199058872111104
# queuesecret = lc4levem8p64n1clkc2pmlwtxsxac81e



# sh mqadmin consumeMessage -n <namesrvAddr> -t <topic> -g <consumerGroup>
.\mqadmin.cmd topicStatus -n "uspro-opdmq-broker1.aqara.com:9876" -t 116919905883855667241b3f
.\mqadmin.cmd topicRoute -n "uspro-opdmq-broker1.aqara.com:9876" -t 116919905883855667241b3f
{
    "brokerDatas":[
        {
            "brokerAddrs":{0:"uspro-opdmq-broker1.aqara.com:10911"
            },
            "brokerName":"broker-a",
            "cluster":"aiot",
            "enableActingMaster":false
        }
    ],
    "filterServerTable":{},
    "queueDatas":[
        {
            "brokerName":"broker-a",
            "perm":6,
            "readQueueNums":8,
            "topicSysFlag":0,
            "writeQueueNums":8
        }
    ]
}

.\mqadmin.cmd statsAll -n uspro-opdmq-broker1.aqara.com:9876 -t 116919905883855667241b3f
#Topic                                                            #Consumer Group                                                  #Accumulation      #InTPS     #OutTPS   #InMsg24Hour  #OutMsg24Hour
116919905883855667241b3f                                          116919905883855667241b3f                                                    0        0.00        0.00              0              0

.\mqadmin.cmd consumeMessage -b broker-a -g 116919905883855667241b3f -t 116919905883855667241b3f -n uspro-opdmq-broker1.aqara.com:9876 -i 2
.\mqadmin.cmd setConsumeMode

.\mqadmin.cmd topicClusterList -n "uspro-opdmq-broker1.aqara.com:9876" -t 116919905883855667241b3f
.\mqadmin.cmd brokerStatus -b broker-a -n uspro-opdmq-broker1.aqara.com:9876
.\mqadmin.cmd brokerConsumeStats -b broker-a -o 116919905883855667241b3f -n uspro-opdmq-broker1.aqara.com:9876
.\mqadmin.cmd consumerStatus -b broker-a -g 116919905883855667241b3f -n uspro-opdmq-broker1.aqara.com:9876


.\mqadmin.cmd consumeMessage -b broker-a -g 116919905883855667241b3f -t 116919905883855667241b3f -n uspro-opdmq-broker1.aqara.com:9876 -i 2
sh mqadmin consumeMessage -b broker-a -g 116919905883855667241b3f -t 116919905883855667241b3f -n uspro-opdmq-broker1.aqara.com:9876 -i 2


#    updateTopic                         Update or create topic.
#    deleteTopic                         Delete topic from broker and NameServer.
#    updateSubGroup                      Update or create subscription group.
#    setConsumeMode                      Set consume message mode. pull/pop etc.
#    deleteSubGroup                      Delete subscription group from broker.
#    updateBrokerConfig                  Update broker's config.
#    updateTopicPerm                     Update topic perm.
#    topicRoute                          Examine topic route info.
#    topicStatus                         Examine topic Status info.
#    topicClusterList                    Get cluster info for topic.
#    addBroker                           Add a broker to specified container.
#    removeBroker                        Remove a broker from specified container.
#    resetMasterFlushOffset              Reset master flush offset in slave.
#    brokerStatus                        Fetch broker runtime status data.
#    queryMsgById                        Query Message by Id.
#    queryMsgByKey                       Query Message by Key.
#    queryMsgByUniqueKey                 Query Message by Unique key.
#    queryMsgByOffset                    Query Message by offset.
#    queryMsgTraceById                   Query a message trace.
#    printMsg                            Print Message Detail.
#    printMsgByQueue                     Print Message Detail by queueId.
#    sendMsgStatus                       Send msg to broker.
#    brokerConsumeStats                  Fetch broker consume stats data.
#    producerConnection                  Query producer's socket connection and client version.
#    consumerConnection                  Query consumer's socket connection, client version and subscription.
#    consumerProgress                    Query consumer's progress, speed.
#    consumerStatus                      Query consumer's internal data structure.
#    cloneGroupOffset                    Clone offset from other group.
#    producer                            Query producer's instances, connection, status, etc.
#    clusterList                         List cluster infos.
#    topicList                           Fetch all topic list from name server.
#    updateKvConfig                      Create or update KV config.
#    deleteKvConfig                      Delete KV config.
#    wipeWritePerm                       Wipe write perm of broker in all name server you defined in the -n param.
#    addWritePerm                        Add write perm of broker in all name server you defined in the -n param.
#    resetOffsetByTime                   Reset consumer offset by timestamp(without client restart).
#    skipAccumulatedMessage              Skip all messages that are accumulated (not consumed) currently.
#    updateOrderConf                     Create or update or delete order conf.
#    cleanExpiredCQ                      Clean expired ConsumeQueue on broker.
#    deleteExpiredCommitLog              Delete expired CommitLog files.
#    cleanUnusedTopic                    Clean unused topic on broker.
#    startMonitoring                     Start Monitoring.
#    statsAll                            Topic and Consumer tps stats.
#    allocateMQ                          Allocate MQ.
#    checkMsgSendRT                      Check message send response time.
#    clusterRT                           List All clusters Message Send RT.
#    getNamesrvConfig                    Get configs of name server.
#    updateNamesrvConfig                 Update configs of name server.
#    getBrokerConfig                     Get broker config by cluster or special broker.
#    getConsumerConfig                   Get consumer config by subscription group name.
#    queryCq                             Query cq command.
#    sendMessage                         Send a message.
#    consumeMessage                      Consume message.
#    updateAclConfig                     Update acl config yaml file in broker.
#    deleteAclConfig                     Delete Acl Config Account in broker.
#    clusterAclConfigVersion             List all of acl config version information in cluster.
#    updateGlobalWhiteAddr               Update global white address for acl Config File in broker.
#    getAclConfig                        List all of acl config information in cluster.
#    updateStaticTopic                   Update or create static topic, which has fixed number of queues.
#    remappingStaticTopic                Remapping static topic.
#    exportMetadata                      Export metadata.
#    exportConfigs                       Export configs.
#    exportMetrics                       Export metrics.
#    exportMetadataInRocksDB             export RocksDB kv config (topics/subscriptionGroups)
#    haStatus                            Fetch ha runtime status data.
#    getSyncStateSet                     Fetch syncStateSet for target brokers.
#    getBrokerEpoch                      Fetch broker epoch entries.
#    getControllerMetaData               Get controller cluster's metadata.
#    getControllerConfig                 Get controller config.
#    updateControllerConfig              Update controller config.
#    electMaster                         Re-elect the specified broker as master.
#    cleanBrokerMetadata                 Clean metadata of broker on controller.
#    dumpCompactionLog                   Parse compaction log to message.
#    getColdDataFlowCtrInfo              Get cold data flow ctr info.
#    updateColdDataFlowCtrGroupConfig    Add or update cold data flow ctr group config.
#    removeColdDataFlowCtrGroupConfig    Remove consumer from cold ctr config.
#    setCommitLogReadAheadMode           Set read ahead mode for all commitlog files.