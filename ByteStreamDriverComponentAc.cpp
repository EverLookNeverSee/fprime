#include <stdio.h>

#include <FpConfig.hpp>

#include <Drv/ByteStreamDriverModel/ByteStreamDriverComponentAc.hpp>

#include <Fw/Types/Assert.hpp>

#if FW_ENABLE_TEXT_LOGGING

#include <Fw/Types/String.hpp>

#endif



namespace Drv {


  // ----------------------------------------------------------------------

  // Getters for numbers of input ports

  // ----------------------------------------------------------------------


  Drv::InputByteStreamSendPort *ByteStreamDriverModelComponentBase ::

    get_send_InputPort(NATIVE_INT_TYPE portNum)

  {

    FW_ASSERT(portNum < this->getNum_send_InputPorts(),static_cast<AssertArg>(portNum));

    return &this->m_send_InputPort[portNum];

  }


  Drv::InputByteStreamPollPort *ByteStreamDriverModelComponentBase ::

    get_poll_InputPort(NATIVE_INT_TYPE portNum)

  {

    FW_ASSERT(portNum < this->getNum_poll_InputPorts(),static_cast<AssertArg>(portNum));

    return &this->m_poll_InputPort[portNum];

  }


  // ----------------------------------------------------------------------

  // Typed connectors for output ports

  // ----------------------------------------------------------------------


  void ByteStreamDriverModelComponentBase ::

    set_recv_OutputPort(

        NATIVE_INT_TYPE portNum,

        Drv::InputByteStreamRecvPort* port

    )

  {

    FW_ASSERT(portNum < this->getNum_recv_OutputPorts(),static_cast<AssertArg>(portNum));

    this->m_recv_OutputPort[portNum].addCallPort(port);

  }


  void ByteStreamDriverModelComponentBase ::

    set_ready_OutputPort(

        NATIVE_INT_TYPE portNum,

        Drv::InputByteStreamReadyPort* port

    )

  {

    FW_ASSERT(portNum < this->getNum_ready_OutputPorts(),static_cast<AssertArg>(portNum));

    this->m_ready_OutputPort[portNum].addCallPort(port);

  }


  void ByteStreamDriverModelComponentBase ::

    set_allocate_OutputPort(

        NATIVE_INT_TYPE portNum,

        Fw::InputBufferGetPort* port

    )

  {

    FW_ASSERT(portNum < this->getNum_allocate_OutputPorts(),static_cast<AssertArg>(portNum));

    this->m_allocate_OutputPort[portNum].addCallPort(port);

  }


  void ByteStreamDriverModelComponentBase ::

    set_deallocate_OutputPort(

        NATIVE_INT_TYPE portNum,

        Fw::InputBufferSendPort* port

    )

  {

    FW_ASSERT(portNum < this->getNum_deallocate_OutputPorts(),static_cast<AssertArg>(portNum));

    this->m_deallocate_OutputPort[portNum].addCallPort(port);

  }


  // ----------------------------------------------------------------------

  // Serialization connectors for output ports

  // ----------------------------------------------------------------------


#if FW_PORT_SERIALIZATION


  void ByteStreamDriverModelComponentBase ::

    set_recv_OutputPort(

        NATIVE_INT_TYPE portNum,

        Fw::InputSerializePort *port

    )

  {

    FW_ASSERT(portNum < this->getNum_recv_OutputPorts(),static_cast<AssertArg>(portNum));

    return this->m_recv_OutputPort[portNum].registerSerialPort(port);

  }
