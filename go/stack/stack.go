package stack

import (
	"sync"

	"github.com/cheekybits/genny/generic"
)

//go:generate go run github.com/cheekybits/genny  -in=$GOFILE -out=gen-$GOFILE gen "Item=int"

// Item the type of the Set
type Item generic.Type

type ItemStack struct {
	items  []Item
	rwLock sync.RWMutex
}

// https://codeburst.io/slice-based-stack-implementation-in-golang-8140603a1dc2
func (stack *ItemStack) Push(t Item) {
	if stack.items == nil {
		stack.items = []Item{}
	}
	stack.rwLock.Lock()
	stack.items = append(stack.items, t)
	stack.rwLock.Unlock()
}

func (stack *ItemStack) Pop() *Item {
	if len(stack.items) == 0 {
		return nil
	}
	stack.rwLock.Lock()
	item := stack.items[len(stack.items)-1]
	stack.items = stack.items[0 : len(stack.items)-1]
	stack.rwLock.Unlock()
	return &item
}

func (stack *ItemStack) Size() int {
	stack.rwLock.RLock()
	defer stack.rwLock.RUnlock()
	return len(stack.items)
}

func (stack *ItemStack) All() []Item {
	stack.rwLock.RLock()
	defer stack.rwLock.RUnlock()
	return stack.items
}

func (stack *ItemStack) IsEmpty() bool {
	stack.rwLock.RLock()
	defer stack.rwLock.RUnlock()
	return len(stack.items) == 0
}
