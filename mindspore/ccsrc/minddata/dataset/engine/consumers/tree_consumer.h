/**
 * Copyright 2020 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef MINDSPORE_CCSRC_MINDDATA_DATASET_ENGINE_CONSUMER_TREE_CONSUMER_H_
#define MINDSPORE_CCSRC_MINDDATA_DATASET_ENGINE_CONSUMER_TREE_CONSUMER_H_

#include <memory>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
#include "minddata/dataset/engine/tree_adapter.h"

namespace mindspore::dataset {
// Forward declare
class TreeAdapter;

namespace api {
class Dataset;
}

/// A base class for tree consumers which would fetch rows from the tree pipeline
class TreeConsumer {
 public:
  /// Constructor that prepares an empty tree_adapter
  TreeConsumer();
  /// Initializes the consumer, this involves constructing and preparing the tree.
  /// \param d The dataset node that represent the root of the IR tree.
  /// \return Status error code.
  virtual Status Init(std::shared_ptr<api::Dataset> d);

 protected:
  /// The class owns the tree_adapter that handles execution tree operations.
  std::unique_ptr<TreeAdapter> tree_adapter_;
  /// Method to return the name of the consumer
  /// \return string
  virtual std::string Name() = 0;
};

/// Consumer that iterates over the dataset and returns the rows one by one as a vector or a map
class IteratorConsumer : public TreeConsumer {
 public:
  /// Constructor which will call the base class default constructor.
  /// \param num_epochs number of epochs. Default to -1 (infinite epochs).
  explicit IteratorConsumer(int32_t num_epochs = -1) : TreeConsumer(), num_epochs_(num_epochs) {}

  Status Init(std::shared_ptr<api::Dataset> d) override;

  /// Returns the next row in a vector format
  /// \param[out] out std::vector of Tensors
  /// \return Status error code
  Status GetNextAsVector(std::vector<TensorPtr> *out);

  /// Returns the next row in as a map
  /// \param[out] out std::map of string to Tensor
  /// \return Status error code
  Status GetNextAsMap(std::unordered_map<std::string, TensorPtr> *out);

 protected:
  /// Method to return the name of the consumer
  /// \return string
  std::string Name() override { return "IteratorConsumer"; }

 private:
  int32_t num_epochs_;
};

/// Consumer that iterates over the dataset and writes it to desk
class SaveToDesk : public TreeConsumer {
 public:
  /// Constructor which will call the base class default constructor.
  /// \param dataset_path path the the dataset
  /// \param num_files number of files. Default to 1
  /// \param dataset_type The format of the dataset. Default to "mindrecod".
  explicit SaveToDesk(std::string dataset_path, int32_t num_files = 1, std::string dataset_type = "mindrecord")
      : TreeConsumer(), dataset_path_(dataset_path), num_files_(num_files), dataset_type_(dataset_type) {}

  /// Save the given dataset to MindRecord format on desk. This is a blocking method (i.e., after returning, all rows
  /// would be written to desk)
  /// \return  Status error code
  Status Save() { return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet."); }

 private:
  std::string dataset_path_;
  int32_t num_files_;
  std::string dataset_type_;
};

/// Consumer that iterates over the dataset and send it to a device
class ToDevice : public TreeConsumer {
 public:
  ToDevice(std::string device_type, bool send_epoch_end, int32_t num_epochs)
      : TreeConsumer(), device_type_(device_type), send_epoch_end_(send_epoch_end), num_epochs_(num_epochs) {}

  Status Init(std::shared_ptr<api::Dataset> d) override;

  Status Send() {
    // TODO(CRC): launch the tree
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
  Status Stop() {
    // TODO(CRC): Get root + call StopSend
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
  Status Continue() {
    // TODO(CRC): Get root + call StopSend
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }

 private:
  std::string device_type_;
  bool send_epoch_end_;
  int32_t num_epochs_;
};

/// Consumer that is used to get some pipeline information
class TreeGetters : public TreeConsumer {
  Status GetDatasetSize(int32_t *size) {
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
  Status GetBatchSize(int32_t *batch_size) {
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
  Status GetRepeatCount(int32_t *repeat_count) {
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
  Status GetNumClasses(int32_t *num_classes) {
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
  Status GetOutputShapes(std::vector<TensorShape> *shapes) {
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
  Status GetOutputTypes(std::vector<DataType> *types) {
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
  Status GetOutputNames(std::vector<std::string> *names) {
    return Status(StatusCode::kNotImplementedYet, __LINE__, __FILE__, "Method is not implemented yet.");
  }
};

}  // namespace mindspore::dataset
#endif  // MINDSPORE_CCSRC_MINDDATA_DATASET_ENGINE_CONSUMER_TREE_CONSUMER_H_
