import os
import copy
import torch
import pytorch_lightning as pl
#from transq.modules.gallery import Gallery
from transq.config import ex
from transq.modules import TransformerSQ,TransformerSQ_CNN
from transq.datamodules.multitask_datamodule import MTDataModule

import warnings


@ex.automain
def main(_config):
    warnings.filterwarnings("ignore", category=UserWarning)
    torch.multiprocessing.set_start_method('spawn', force=True)
    _config = copy.deepcopy(_config)
    print(_config)
    pl.seed_everything(_config["seed"])

    dm = MTDataModule(_config, dist=True)
    
    tokenizer = dm.tokenizer
    vocab_size = dm.vocab_size
 
    if _config["backbone"]=="ViT":
        model = TransformerSQ(_config, tokenizer)
    elif _config["backbone"]=="CNN":
        model = TransformerSQ_CNN(_config, tokenizer)
    #print(model)
    exp_name = f'{_config["exp_name"]}'

    os.makedirs(_config["log_dir"], exist_ok=True)
    checkpoint_callback = pl.callbacks.ModelCheckpoint(
        #dirpath="/fast-disk/kongming/Code/TranSQ/result/",
        save_top_k=1,
        verbose=True,
        monitor="val/the_metric",
        #monitor="val/loss",
        mode="max",
        save_last=True,
    )
    logger = pl.loggers.TensorBoardLogger(
        _config["log_dir"],
        name=f'{exp_name}_seed{_config["seed"]}_from_{_config["load_path"].split("/")[-1][:-5]}',
    )

    lr_callback = pl.callbacks.LearningRateMonitor(logging_interval="step")
    callbacks = [checkpoint_callback, lr_callback]

    num_gpus = (
        _config["num_gpus"]
        if isinstance(_config["num_gpus"], int)
        else len(_config["num_gpus"])
    )

    grad_steps = _config["batch_size"] // (
        _config["per_gpu_batchsize"] * num_gpus * _config["num_nodes"]
    )

    max_steps = _config["max_steps"] if _config["max_steps"] is not None else None
    
    print("start trainer process...")
    
    trainer = pl.Trainer(
        gpus=_config["num_gpus"],
        num_nodes=_config["num_nodes"],
        precision=_config["precision"],
        accelerator="ddp",
        benchmark=True,
        deterministic=True,
        max_epochs=_config["max_epoch"] if max_steps is None else 1000,
        max_steps=max_steps,
        callbacks=callbacks,
        #callbacks=[checkpoint_callback],
        logger=logger,
        prepare_data_per_node=False,
        replace_sampler_ddp=False,
        accumulate_grad_batches=grad_steps,
        log_every_n_steps=10,
        flush_logs_every_n_steps=10,
        resume_from_checkpoint=_config["resume_from"],
        weights_summary="top",
        fast_dev_run=_config["fast_dev_run"],
        val_check_interval=_config["val_check_interval"],
        #check_val_every_n_epoch=3.0
    )

    if not _config["test_only"]:
        trainer.fit(model, datamodule=dm)
    else:
        trainer.test(model, datamodule=dm)
