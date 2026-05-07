import argparse
import cv2
import time
import threading
from queue import Queue
from ultralytics import YOLO
import torch

class VideoCaptureRAII:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Не удалось открыть видео: {video_path}")

    def __enter__(self):
        return self.cap

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cap.release()


class VideoWriterRAII:
    def __init__(self, output_path, fps, frame_size):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    def __enter__(self):
        return self.writer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.writer.release()


def worker_thread(input_queue, output_queue, model_path='yolov8s-pose.pt'):
    """
    Поток-обработчик кадров.
    Каждый поток создает СВОЮ собственную модель YOLO.
    """
    with torch.inference_mode():
        model = YOLO(model_path)
        while True:
            item = input_queue.get()
            if item is None:
                input_queue.put(None)
                break

            frame_idx, frame = item
            results = model(frame, verbose=False)
            processed_frame = results[0].plot()

            output_queue.put((frame_idx, processed_frame))


def process_video_multithreaded(video_path, output_path, num_threads=4):
    print(f"\nМногопоточная обработка ({num_threads} потоков)...")

    with VideoCaptureRAII(video_path) as cap:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        input_queue = Queue(maxsize=num_threads * 2)
        output_queue = Queue()

        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=worker_thread,
                                 args=(input_queue, output_queue, i))
            t.start()
            threads.append(t)

        start_time = time.time()

        frame_idx = 0
        frames_dict = {}  # Для восстановления порядка
        processed_frames_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            input_queue.put((frame_idx, frame.copy()))
            frame_idx += 1
        input_queue.put(None)

        while processed_frames_count < frame_idx:
            if not output_queue.empty():
                idx, processed_frame = output_queue.get()
                frames_dict[idx] = processed_frame
                processed_frames_count += 1

        for t in threads:
            t.join()

        processing_time = time.time() - start_time

        processed_frames = [frames_dict[i] for i in range(frame_idx)]

        with VideoWriterRAII(output_path, fps, frame_size) as writer:
            for frame in processed_frames:
                writer.write(frame)

    return processing_time


def process_video_single_threaded(video_path, output_path):
    print("\nОднопоточная обработка...")

    with VideoCaptureRAII(video_path) as cap:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        model = YOLO('yolov8s-pose.pt')

        frames = []
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results = model(frame, verbose=False)
            processed_frame = results[0].plot()
            frames.append(processed_frame)

        processing_time = time.time() - start_time
        with VideoWriterRAII(output_path, fps, frame_size) as writer:
            for frame in frames:
                writer.write(frame)

    return processing_time


# def find_optimal_threads(video_path, max_threads=8):
#     print("\n=== Поиск оптимального количества потоков ===\n")
#
#     results = []
#
#     for num_threads in range(1, max_threads + 1):
#         test_output = f"test_{num_threads}_threads.mp4"
#         time_taken = process_video_multithreaded(video_path, test_output, num_threads)
#         results.append((num_threads, time_taken))
#         print(f"Потоков: {num_threads}, Время: {time_taken:.2f} сек")
#     optimal = min(results, key=lambda x: x[1])
#     print(f"\nОптимальное количество потоков: {optimal[0]} (время: {optimal[1]:.2f} сек)")
#
#     return optimal[0]


def main():
    parser = argparse.ArgumentParser(description='Обработка видео с YOLOv8-pose')
    parser.add_argument('--video', type=str, required=True,
                        help='Путь к входному видео (640x480)')
    parser.add_argument('--mode', type=str, required=True,
                        choices=['single', 'multi', 'auto'],
                        help='Режим: single (один поток), multi (много потоков), auto (поиск оптимального)')
    parser.add_argument('--output', type=str, required=True,
                        help='Имя выходного видеофайла')
    parser.add_argument('--threads', type=int, default=4,
                        help='Количество потоков (для режима multi)')

    args = parser.parse_args()

    if args.mode == 'single':
        proc_time = process_video_single_threaded(args.video, args.output)
        print(f"\nОбработка завершена!")
        print(f"Время выполнения: {proc_time:.2f} секунд")
        print(f"Результат сохранен в: {args.output}")

    elif args.mode == 'multi':
        proc_time = process_video_multithreaded(args.video, args.output, args.threads)
        print(f"\nОбработка завершена!")
        print(f"Время выполнения: {proc_time:.2f} секунд")
        print(f"Результат сохранен в: {args.output}")

    # elif args.mode == 'auto':
    #     optimal_threads = find_optimal_threads(args.video, args.output)
    #     print(f"\nФинальная обработка с {optimal_threads} потоками")
    #     proc_time = process_video_multithreaded(args.video, args.output, optimal_threads)
    #     print(f"\nОбработка завершена!")
    #     print(f"Время выполнения: {proc_time:.2f} секунд")
    #     print(f"Результат сохранен в: {args.output}")


if __name__ == '__main__':
    main()