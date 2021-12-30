package main

import (
	"fmt"
	"ka/m/util"
	"path/filepath"
	"strconv"
)

type Literal struct {
	Version int64
	TypeId  int64
	Value   int64
}

type Operator struct {
	Version  int64
	TypeId   int64
	Value    int64
	LengthId int64
	Length   int64
	Packets  []interface{}
}

const (
	TYPE_LITERAL = 4
)

func PrintPacket(p interface{}) string {
	switch p.(type) {
	case Operator:
		packet := p.(Operator)
		subpackets := ""
		for _, sp := range packet.Packets {
			subpackets += PrintPacket(sp)
		}
		return fmt.Sprintf("[Operator Packet] Version: %v TypeId: %v Value: %v LengthId: %v, Length: %v \n\t %v", packet.Version, packet.TypeId, packet.Value, packet.LengthId, packet.Length, subpackets)
	case Literal:
		packet := p.(Literal)
		return fmt.Sprintf("[Literal Packet] Version: %v TypeId: %v Value: %v \n", packet.Version, packet.TypeId, packet.Value)
	}
	return ""
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

func ReadPacket(input string, startPos int) (l interface{}, c int) {
	var count int
	n := startPos

	version, count, _ := ReadBits(input, n, 3)
	n += count

	typeId, count, _ := ReadBits(input, n, 3)
	n += count

	switch typeId {
	case TYPE_LITERAL:
		value, count := ReadNumber(input, n)
		n += count
		return Literal{
			Version: version,
			TypeId:  typeId,
			Value:   value,
		}, n - startPos
	default:
		lengthId, count, _ := ReadBits(input, n, 1)
		n += count

		op := Operator{
			Version:  version,
			TypeId:   typeId,
			LengthId: lengthId,
			Length:   0,
			Packets:  nil,
		}

		if lengthId == 0 {
			length, count, _ := ReadBits(input, n, 15)
			n += count

			op.Length = length

			subpacketStart := n
			for n-subpacketStart < int(length) {
				packet, count := ReadPacket(input, n)
				n += count
				op.Packets = append(op.Packets, packet)
			}
		} else {
			length, count, _ := ReadBits(input, n, 11)
			n += count

			op.Length = length

			for i := int64(0); i < length; i++ {
				packet, count := ReadPacket(input, n)
				n += count
				op.Packets = append(op.Packets, packet)
			}
		}
		return op, n - startPos
	}
}

// Takes a binary string, e.g. 011111100101
// @returns an int64 representing the conversion from start to count + start
func ReadBits(packet string, start, count int) (int64, int, error) {
	bits, err := strconv.ParseInt(packet[start:start+count], 2, 64)
	return bits, count, err
}

func ReadNumber(input string, startPos int) (out int64, count int) {
	for {
		part, _, err := ReadBits(input, startPos, 5)
		if err != nil {
			fmt.Printf(`failed to ReadNumber. %v %v`, input, startPos)
		}
		out <<= 4
		out |= int64(part & 0x0f)
		startPos += 5
		count += 5
		if part&0x10 == 0 {
			break
		}
	}
	return out, count
}

func SumVersions(packet interface{}) int64 {
	var sum int64
	switch p := packet.(type) {
	case Literal:
		sum += p.Version
	case Operator:
		sum += p.Version
		for _, sp := range p.Packets {
			sum += SumVersions(sp)
		}
	}
	return sum
}

func Part1(data string) int {
	bitData := data

	packets, _ := ReadPacket(bitData, 0)
	// fmt.Println(PrintPacket(packets))

	return int(SumVersions(packets))
}

func Part2(data string) int {
	return 0
}

func main() {
	input := filepath.Join("2021", "day_16", "raw-input.txt")
	inputData := util.ParseInput(input)
	bitData := ProcessInput(inputData[0])
	p1Result := Part1(bitData)
	fmt.Printf("Part I: the sum of versions is = %v\n", p1Result)
	if p1Result != 1007 {
		panic("FAILED on Part I ")
	}

	p2Result := Part2(bitData)
	fmt.Printf("Part II: the lowest risk path level is = %v\n", p2Result)
	if p2Result != 2874 {
		panic("FAILED on Part II")
	}
}
