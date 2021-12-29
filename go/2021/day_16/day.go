package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"strconv"
)

type Packet struct {
	Version   int64
	TypeId    int64
	Value     string
	SubPacket *Packet
}

type Bits struct {
	Packet
}

const (
	TYPE_LITERAL = 4
)

func (p *Packet) String() string {
	return fmt.Sprintf("[Packet] Version: %v TypeId: %v Value: %v \nSubPacket: %v", p.Version, p.TypeId, p.Value, p.SubPacket)
}

func (b *Bits) CountSubPackets() int {
	packets := 0
	for p := b.SubPacket; p != nil; {
		packets += 1
		p = p.SubPacket
	}
	return packets
}

func (b *Bits) SumVersions() int {
	versionSum := int(b.Version)
	for p := b.SubPacket; p != nil; {
		versionSum += int(p.Version)
		p = p.SubPacket
	}
	return versionSum
}

func (p *Packet) ProcessLiteral(input string) (string, int64, error) {
	remainingPackets := input
	for i := 0; i < len(input); i += 5 {
		max := i + 5
		if max > len(input) {
			max = len(input) - 1
		}
		pv := input[i:max][1:]
		if pv != "0" {
			p.Value += pv
		}
		if input[i:max][0:1] == "0" {
			fmt.Println("Last bits for literal ", pv)
			remainingPackets = remainingPackets[max:]
			break
		}
	}
	lv, err := strconv.ParseInt(p.Value, 2, 64)
	return remainingPackets, lv, err
}

func (p *Packet) ProcessOperator(input string) (string, int, error) {
	lengthTypeId := input[0:1]
	remainingPackets := ""
	remainingPacketCount := -1
	var err error
	if len(lengthTypeId) != 1 {
		err = fmt.Errorf(`error finding length type id`)
	}
	fmt.Println("Length type ID: ", lengthTypeId)
	fmt.Println("ProcessOperator: ", input[1:])
	switch lengthTypeId {
	case "0":
		chop := 15
		subpacketLength, e := ReadBitsFromPacket(input[1:], 0, chop)
		if e != nil {
			err = fmt.Errorf(`failed to read subpacket length for type %v`, lengthTypeId)
		}
		subpackets := input[chop+1 : chop+int(subpacketLength)+1]
		remainingPackets = subpackets
	case "1":
		chop := 11
		subpacketCount, e := ReadBitsFromPacket(input[1:], 0, chop)
		if e != nil {
			err = fmt.Errorf(`failed to read subpacket length for type %v`, lengthTypeId)
		}
		remainingPacketCount = int(subpacketCount)
		subpackets := input[chop+1:]
		remainingPackets = subpackets
	}
	return remainingPackets, remainingPacketCount, err
}

// Takes hexidecimal input and converts to binary with 4 bits per byte
func ProcessInput(data string) string {
	inputStr := ""
	for _, char := range data {
		v, _ := strconv.ParseInt(string(char), 16, 64)
		inputStr += fmt.Sprintf("%04b", v)
		// fmt.Printf("Hex value %s converted to dec: %04b\n", string(char), v)
	}
	return inputStr
}

// read the bits from a packet from start, end into digit
func ReadBitsFromPacket(packet string, start int, end int) (int64, error) {
	bits, err := strconv.ParseInt(packet[start:end], 2, 64)
	return bits, err
}

func GetPacketVersion(input string) int64 {
	version, err := ReadBitsFromPacket(input, 0, 3)
	if err != nil {
		panic("Failed to convert to version")
	}
	return version
}

func GetPacketTypeId(input string) int64 {
	typeId, err := ReadBitsFromPacket(input, 3, 6)
	if err != nil {
		panic("Failed to convert to typeId")
	}
	return typeId
}

func (p *Packet) ProcessPackets(remainingPackets string, remainingPacketCount int) (string, error) {
	// max := 10
	var err error
	if len(remainingPackets) == 0 {
		fmt.Println("END")
		p = nil
		return remainingPackets, err
	} else {
		fmt.Println("ProcessPackets RR:", len(remainingPackets), remainingPackets, remainingPacketCount)

		p.Version = GetPacketVersion(remainingPackets)
		p.TypeId = GetPacketTypeId(remainingPackets)
		p.Value = remainingPackets[6:]
		var rp string
		var rpc int
		var e error
		var lv int64

		if p.TypeId == TYPE_LITERAL {
			fmt.Println("****Literal")
			rp, lv, e = p.ProcessLiteral(remainingPackets[6:])
			if e != nil {
				err = fmt.Errorf("failed to convert to literal value")
				return rp, err
			}
			fmt.Printf("%d\n", lv)
		} else {
			// operator packets
			rp, rpc, e = p.ProcessOperator(remainingPackets[6:])
			if e != nil {
				err = fmt.Errorf("failed to process operator packet")
				return rp, err
			}
		}
		p.SubPacket = &Packet{}
		fmt.Printf("RR2: %d %s %d\n", len(rp), rp, rpc)
		return p.SubPacket.ProcessPackets(rp, rpc)
	}
	// for i := 0; len(remainingPackets) > 0 && i < max; i++ {
	// 	fmt.Println("ProcessPackets RR:", i, remainingPackets, remainingPacketCount)

	// 	p.Version = GetPacketVersion(remainingPackets)
	// 	p.TypeId = GetPacketTypeId(remainingPackets)
	// 	if p.TypeId == TYPE_LITERAL {
	// 		fmt.Println("****Literal")
	// 		remainingPackets, lv, err := p.ProcessLiteral(remainingPackets[6:])
	// 		if err != nil {
	// 			panic("Failed to convert to literal value")
	// 		}
	// 		fmt.Printf("%d %s\n", lv, remainingPackets)
	// 		break
	// 	} else {
	// 		// operator packets
	// 		p.SubPacket = &Packet{}
	// 		remainingPackets, _, err := p.ProcessOperator(remainingPackets[6:])
	// 		p.Value = remainingPackets
	// 		if err != nil {
	// 			panic("Failed to process operator packet")
	// 		}
	// 		if len(remainingPackets) > 0 {
	// 			p.SubPacket.ProcessPackets(remainingPackets, remainingPacketCount)
	// 		}
	// 	}

	// 	fmt.Printf("RR2: %s %d\n", remainingPackets, remainingPacketCount)
	// }
	// return remainingPackets, err
}

func Part1(data string) int {
	bitData := data
	fmt.Println("***********")
	fmt.Println("***********")
	fmt.Println("***********")
	fmt.Println("Process for: ", bitData)

	bits := Bits{
		Packet: Packet{
			SubPacket: &Packet{},
		},
	}
	_, err := bits.ProcessPackets(bitData, -1)
	if err != nil {
		panic("Failed to process packets")
	}
	fmt.Println(bits.String())

	return bits.SumVersions()
}

func Part2(data string) int {
	return 0
}

func main() {
	input := filepath.Join("2021", "day_16", "raw-input.txt")
	inputData := util.ParseInput(input)
	p1Result := Part1(inputData[0])
	fmt.Printf("Part I: the lowest risk path level is = %v\n", p1Result)
	if p1Result != 562 {
		panic("FAILED on Part I")
	}

	p2Result := Part2(inputData[0])
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
