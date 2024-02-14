# Boiler plate stuff to start the module
import jpype
import jpype.imports
from jpype.types import *
from time import time, sleep
import threading

# Launch the JVM
jpype.startJVM(classpath=['lib/rocketmq-all-5.1.4-bin-release/lib/*'], convertStrings=True)

from org.apache.rocketmq.acl.common import AclClientRPCHook;
from org.apache.rocketmq.acl.common import SessionCredentials;
from org.apache.rocketmq.client.consumer import DefaultMQPushConsumer;
from org.apache.rocketmq.client.consumer.listener import ConsumeConcurrentlyContext;
from org.apache.rocketmq.client.consumer.listener import ConsumeConcurrentlyStatus;
from org.apache.rocketmq.client.consumer.listener import MessageListenerConcurrently;
from org.apache.rocketmq.client.consumer.rebalance import AllocateMessageQueueAveragely;
from org.apache.rocketmq.client.exception import MQClientException;
from org.apache.rocketmq.common import UtilAll;
from org.apache.rocketmq.common.consumer import ConsumeFromWhere;
from org.apache.rocketmq.common.message import MessageExt;
from java.lang import System


mqAddress:str = "uspro-opdmq-broker1.aqara.com:9876"
appId:str = "116919905883855667241b3f"
keyId:str = "K.1169199058872111104"
appKey:str = "lc4levem8p64n1clkc2pmlwtxsxac81e"


@jpype.JImplements(MessageListenerConcurrently)
class AqaraMessageListener():
    def __init__(self):
        pass

    @jpype.JOverride
    def consumeMessage(msgs, context):
        try:
            for messageExt in msgs:
                topic = messageExt.getTopic()
                tag = messageExt.getTags()
                message = messageExt.getBody()

                System.out.println("Received Message: " + message)
        except:
            System.out.println("Error processing message: " + msgs)

        return ConsumeConcurrentlyStatus.CONSUME_SUCCESS

def start():
    print("Creating hook")
    acl = AclClientRPCHook(SessionCredentials(keyId, appKey))
    consumer = DefaultMQPushConsumer(appId, acl, AllocateMessageQueueAveragely())

    print("Creating Consumer")
    consumer.setVipChannelEnabled(False)
    consumer.setNamesrvAddr(mqAddress)
    consumer.setConsumeFromWhere(ConsumeFromWhere.CONSUME_FROM_TIMESTAMP)

    consumeTimestamp = "20240106234300"
    print("Consuming from: ", consumeTimestamp)
    consumer.setConsumeTimestamp(consumeTimestamp)

    consumer.subscribe(appId, "*")

    print("Adding Listener")
    consumer.registerMessageListener(AqaraMessageListener())

    # consumer.registerMessageListener(new MessageListenerConcurrently() {
    #     public ConsumeConcurrentlyStatus consumeMessage(List<MessageExt> msgs, ConsumeConcurrentlyContext context) {
    #         try {
    #             for (MessageExt messageExt : msgs) {
    #                 String topic = messageExt.getTopic();
    #                 String tag = messageExt.getTags();
    #                 String msg = new String(messageExt.getBody());

    #                 System.out.println("******device info******" + msg);
    #             }
    #         } catch (Exception e) {
    #             e.printStackTrace();
    #         }

    #         return ConsumeConcurrentlyStatus.CONSUME_SUCCESS;
    #     }
    # });

    print("Starting Consumer")
    consumer.start()

def sleep_function():
    while True:
        print("Thread is sleeping for 10 seconds")
        sleep(10)

# Create a new thread
thread = threading.Thread(target=sleep_function)

start()
thread.start()
