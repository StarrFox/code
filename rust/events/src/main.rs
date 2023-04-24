use std::{
    any::{Any, TypeId},
    collections::HashMap,
};

trait Event: Any {}

type Listener = Box<dyn Fn(&dyn Any)>;
type Listeners = Vec<Listener>;
type ListenerMap = HashMap<TypeId, Listeners>;

struct EventDispatcher {
    listeners: ListenerMap,
}

impl EventDispatcher {
    pub fn new() -> Self {
        Self {
            listeners: HashMap::new(),
        }
    }

    pub fn subscribe<T: Event>(&mut self, callback: fn(&T)) {
        let type_id = TypeId::of::<T>();
        let listeners = self.listeners.entry(type_id).or_insert_with(Vec::new);

        let callback = Box::new(move |e: &dyn Any| {
            if let Some(e) = e.downcast_ref::<T>() {
                callback(e);
            }
        });

        listeners.push(callback);
    }

    pub fn dispatch<T: Event>(&self, event: &T) {
        let type_id = TypeId::of::<T>();
        if let Some(listeners) = self.listeners.get(&type_id) {
            for callback in listeners {
                callback(event);
            }
        }
    }
}

#[derive(Debug)]
pub struct PrintEvent {
    pub message: String,
}

impl Event for PrintEvent {}

fn print_callback(event: &PrintEvent) {
    println!("Print event: {:?}", event);
}

fn main() {
    let mut dispatcher = EventDispatcher::new();
    dispatcher.subscribe(print_callback);

    let event = PrintEvent {
        message: "Hello!".to_string(),
    };

    dispatcher.dispatch(&event);
}
