#ifndef BESS_MODULES_QUEUE_H_
#define BESS_MODULES_QUEUE_H_

#include "../kmod/llring.h"
#include "../module.h"
#include "../module_msg.pb.h"

class Queue final : public Module {
 public:
  static const Commands cmds;

  Queue() : Module(), queue_(), prefetch_(), burst_() {
    propagate_workers_ = false;
  }

  CommandResponse Init(const bess::pb::QueueArg &arg);

  void DeInit() override;

  struct task_result RunTask(void *arg) override;
  void ProcessBatch(bess::PacketBatch *batch) override;

  std::string GetDesc() const override;

  CommandResponse CommandSetBurst(const bess::pb::QueueCommandSetBurstArg &arg);
  CommandResponse CommandSetSize(const bess::pb::QueueCommandSetSizeArg &arg);

  CheckConstraintResult CheckModuleConstraints() const override;

  bool is_task() override { return true; } // Queue overrides RunTask.

 protected:
  struct llring *queue_;

 private:
  int Resize(int slots);
  CommandResponse SetSize(uint64_t size);

  bool prefetch_;
  bool backpressure_;
  int burst_;
  uint64_t size_;
  uint64_t high_water_;
  uint64_t low_water_;
  const double kHighWaterRatio = 0.90;
  const double kLowWaterRatio = 0.15;
  bool underload_;
  bool overload_;
};

#endif  // BESS_MODULES_QUEUE_H_
